from django.db import models
from django.contrib.auth.models import User
from scout.models import Scout
from mbu.models import Counselor, MeritBadgeUniversity

# Models owned by the course app

class Course(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Session(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    mbu = models.ForeignKey(MeritBadgeUniversity)

    def __str__(self):
        return "%s (%s - %s)" % (self.name, str(self.start_time), str(self.end_time))

class CourseInstance(models.Model):
    course = models.ForeignKey(Course)
    session = models.ForeignKey(Session)
    counselor = models.ForeignKey(Counselor, null=True, blank=True)
    enrollees = models.ManyToManyField(User, related_name='enrollees', blank=True)
    teaching_assistants = models.ManyToManyField(User, related_name='teaching_assistants', blank=True)

    def __str__(self):
        return self.course.name + str(self.session)

class WaitingList(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    position_in_line = models.IntegerField()
