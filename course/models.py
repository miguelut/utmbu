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

    def __str__(self):
        return "%s (%s - %s)" % (self.name, str(start_time), str(end_time))

class CourseInstance(models.Model):
    course = models.ForeignKey(Course)
    session = models.ForeignKey(Session)
    counselor = models.ForeignKey(Counselor)
    merit_badge_university = models.ForeignKey(MeritBadgeUniversity)
    teaching_assistants = models.ManyToManyField(User)

    def __str__(self):
        return self.course.name + str(session)

class WaitingList(models.Model):
    scout = models.ForeignKey(Scout)
    course = models.ForeignKey(Course)
    position_in_line = models.IntegerField()
