from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=200)

class Session(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    counselor = models.ForeignKey('mbu.Counselor')
    course = models.ForeignKey('Course')
    #teaching_assistants = models.ManyToManyField(User)
    #merit_badge_university = models.ForeignKey('MeritBadgeUniversity')