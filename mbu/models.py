from django.db import models
from mbu.util import _get_hash_str, _send_sm_request_email
from django.contrib.auth.models import User

# This class will represent the yearly MBU so we can
# retain information across multiple years
class MeritBadgeUniversity(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField()
    current = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' ' + str(self.year)


class Council(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name',)


class Troop(models.Model):
    number = models.CharField(max_length=10)
    council = models.ForeignKey(Council)

    def __str__(self):
        return "%s - %s" % (self.number, self.council)

    class Meta:
        unique_together = ('number', 'council')


class Scout(models.Model):
    user = models.OneToOneField(User)
    troop = models.ForeignKey(Troop, blank=True, null=True)

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
    key = models.CharField(max_length=64, default=_get_hash_str, unique=True)

    def save(self, *args, **kwargs):
        super(ScoutmasterRequest, self).save(args, kwargs)
        _send_sm_request_email(email=self.email, key=self.key)


class Course(models.Model):
    name = models.CharField(max_length=200)
    requirements = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TimeBlock(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    mbu = models.ForeignKey(MeritBadgeUniversity)

    def __str__(self):
        return "%s (%s - %s)" % (self.name, str(self.start_time), str(self.end_time))


class CourseInstance(models.Model):
    course = models.ForeignKey(Course)
    session = models.ForeignKey(TimeBlock)
    counselor = models.CharField(max_length=100)
    enrollees = models.ManyToManyField(User, related_name='enrollments', blank=True)
    teaching_assistants = models.ManyToManyField(User, related_name='assistant_courses', blank=True)
    location = models.CharField(max_length=100)
    max_enrollees = models.IntegerField()

    def __str__(self):
        return self.course.name + str(self.session)
