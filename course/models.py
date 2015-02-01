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
    course = models.ForeignKey(Course)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    counselor = models.ForeignKey(Counselor)
    merit_badge_university = models.ForeignKey(MeritBadgeUniversity)
    teaching_assistants = models.ManyToManyField(User)

class WaitingList(models.Model):
    scout = models.ForeignKey(Scout)
    course = models.ForeignKey(Course)
    position_in_line = models.IntegerField()
