from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from mbu.model_utils import send_sm_request_email, get_hash_str
from rest_framework.serializers import ModelSerializer


# This class will represent the yearly MBU so we can
# retain information across multiple years
class MeritBadgeUniversity(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField()
    current = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' ' + str(self.year)


class Council(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CouncilSerializer(ModelSerializer):
    class Meta:
        model = Council


class Troop(models.Model):
    number = models.IntegerField()
    council = models.ForeignKey('Council')

    def __str__(self):
        return "%s - %s" % (self.number, self.council)

    @property
    def sorted_scouts(self):
        return self.scouts.order_by("user__last_name", "user__first_name")

    class Meta:
        unique_together = ('number', 'council')
        ordering = ['number']


class TroopSerializer(ModelSerializer):
    council = CouncilSerializer(read_only=True)

    class Meta:
        model = Troop
        depth = 1


class Parent(models.Model):
    user = models.OneToOneField(User)
    troop = models.ForeignKey('Troop', null=True)

    def __str__(self):
        return "%d - %s %s" % (self.pk, self.user.first_name, self.user.last_name)

    class Meta:
        permissions = (
            ('parent_edit_scout_schedule', 'Can edit scout schedule'),
            ('edit_parent_profile', 'Can edit parent profile')
        )


class Scout(models.Model):
    user = models.OneToOneField(User)
    troop = models.ForeignKey('Troop', null=True, related_name="scouts")
    rank = models.CharField(max_length=15, choices=settings.SCOUT_RANKS)
    waiver = models.BooleanField(default=False)
    parent = models.ForeignKey('Parent', blank=True, null=True, related_name='scouts')
    checked_in = models.BooleanField(default=False)

    def __str__(self):
        return "%d - %s %s" % (self.pk, self.user.first_name, self.user.last_name)

    @property
    def sorted_enrollments(self):
        return self.enrollments.order_by("timeblock__start_time")

    class Meta:
        permissions = (
            ('edit_scout_schedule', 'Can edit schedule'),
            ('edit_scout_profile', 'Can edit scout profile')
        )
        ordering = ['user']


class Scoutmaster(models.Model):
    user = models.OneToOneField(User)
    troop = models.ForeignKey('Troop', blank=True, null=True)

    def __str__(self):
        return "%d - %s %s" % (self.pk, self.user.first_name, self.user.last_name)

    class Meta:
        permissions = (
            ('can_modify_troop_enrollments', 'Can modify schedules of scouts in own troop.'),
            ('edit_scoutmaster_profile', 'Can edit scoutmaster profile')
        )


class ScoutmasterRequest(models.Model):
    email = models.EmailField(unique=True)
    troop = models.ForeignKey('Troop')
    key = models.CharField(max_length=64, unique=True)

    def save(self, *args, **kwargs):
        self.key = get_hash_str(self.email)
        super(ScoutmasterRequest, self).save(args, kwargs)
        send_sm_request_email(email=self.email, key=self.key, troop=self.troop)


class ScoutmasterRequestAdmin(admin.ModelAdmin):
    exclude = ['key']


class Course(models.Model):
    name = models.CharField(max_length=200)
    requirements = models.CharField(max_length=200)
    image_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course


class TimeBlock(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    mbu = models.ForeignKey('MeritBadgeUniversity')
    double = models.BooleanField(default=False)
    all_day = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s - %s)" % (self.name, str(self.start_time), str(self.end_time))


class TimeBlockSerializer(ModelSerializer):
    class Meta:
        model = TimeBlock


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class ScoutCourseInstance(models.Model):
    course = models.ForeignKey('Course')
    timeblock = models.ForeignKey('TimeBlock')
    counselor = models.CharField(max_length=100)
    enrollees = models.ManyToManyField('Scout', related_name='enrollments', blank=True)
    teaching_assistants = models.ManyToManyField(User, related_name='assistant_courses', blank=True)
    location = models.CharField(max_length=100)
    max_enrollees = models.IntegerField()

    @property
    def status(self):
        if self.max_enrollees - len(self.enrollees.all()) > 0:
            return '%d seats left' % (self.max_enrollees - len(self.enrollees.all()))
        else:
            return 'Full'

    @property
    def sorted_enrollees(self):
        return self.enrollees.order_by("user__last_name", "user__first_name")

    def __str__(self):
        return self.course.name + str(self.timeblock)

    class Meta:
        ordering = ['course__name']


class ScoutCourseInstanceSerializer(ModelSerializer):
    teaching_assistants = UserSerializer(many=True, read_only=True)
    timeblock = TimeBlockSerializer(read_only=True)

    class Meta:
        model = ScoutCourseInstance
        depth = 1


class PaymentSet(models.Model):
    # user = models.ForeignKey(User)
    pp_txn_id = models.CharField(max_length=100, null=True)
    payments = models.ManyToManyField('Payment')


class Payment(models.Model):
    user = models.ForeignKey(User)
    amount = models.DecimalField(decimal_places=2, max_digits=6)
    status = models.CharField(max_length=15)

    def __str__(self):
        return "%d - %s %s: %s %s" % (self.pk, self.user.first_name, self.user.last_name, self.status, self.amount)

    def txn_id(self):
        return PaymentSet.objects.get(payments__id__contains=self.pk).pp_txn_id


class RegistrationStatus(models.Model):
    status = models.CharField(max_length=7, choices=(('OPEN', 'OPEN'), ('CLOSED', 'CLOSED')))

    def __str__(self):
        return 'Status: %s' % self.status

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(RegistrationStatus, self).save(*args, **kwargs)
