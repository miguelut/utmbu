from django.db import models
from django.contrib.auth.models import User
from scout.models import Scout
from mbu.models import Counselor, MeritBadgeUniversity

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Session(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name + '(' + str(start_time) + str(end_time) + ')'

class CourseInstance(models.Model):
    course = models.ForeignKey(Course)
    sessions = models.ManyToManyField(Session)
    counselor = models.ForeignKey(Counselor)
    merit_badge_university = models.ForeignKey(MeritBadgeUniversity)
    teaching_assistants = models.ManyToManyField(User)

    def __str__(self):
        return self.course.name + str(self.start_time)

class WaitingList(models.Model):
    scout = models.ForeignKey(Scout)
    course = models.ForeignKey(Course)
    position_in_line = models.IntegerField()
