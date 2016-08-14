from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from mbu.model_utils import send_sm_request_email, get_hash_str


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


class Troop(models.Model):
    number = models.IntegerField()
    council = models.ForeignKey(Council)

    def __str__(self):
        return "%s - %s" % (self.number, self.council)

    class Meta:
        unique_together = ('number', 'council')


class Scout(models.Model):
    user = models.OneToOneField(User)
    troop = models.ForeignKey(Troop, blank=True, null=True)
    rank = models.CharField(max_length=15)
    waiver = models.BooleanField(default=False)

    def __str__(self):
        return "%d - %s %s" % (self.pk, self.user.first_name, self.user.last_name)

    class Meta:
        permissions = (
            ('edit_scout_schedule', 'Can edit schedule'),
            ('edit_scout_profile', 'Can edit scout profile')
        )


class Scoutmaster(models.Model):
    user = models.OneToOneField(User)
    troop = models.ForeignKey(Troop, blank=True, null=True)

    def __str__(self):
        return "%d - %s %s" % (self.pk, self.user.first_name, self.user.last_name)

    class Meta:
        permissions = (
            ('can_modify_troop_enrollments', 'Can modify schedules of scouts in own troop.'),
            ('edit_scoutmaster_profile', 'Can edit scoutmaster profile')
        )


class ScoutmasterRequest(models.Model):
    email = models.EmailField(unique=True)
    troop = models.ForeignKey(Troop)
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


class TimeBlock(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    mbu = models.ForeignKey(MeritBadgeUniversity)

    def __str__(self):
        return "%s (%s - %s)" % (self.name, str(self.start_time), str(self.end_time))


class ScoutCourseInstance(models.Model):
    course = models.ForeignKey(Course)
    timeblock = models.ForeignKey(TimeBlock)
    counselor = models.CharField(max_length=100)
    enrollees = models.ManyToManyField(Scout, related_name='enrollments', blank=True)
    teaching_assistants = models.ManyToManyField(User, related_name='assistant_courses', blank=True)
    location = models.CharField(max_length=100)
    max_enrollees = models.IntegerField()

    def __str__(self):
        return self.course.name + str(self.timeblock)


class Payment(models.Model):
    timestamp = models.DateTimeField()
    tracking_number = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=6)
    scout = models.ForeignKey(Scout)
