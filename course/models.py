from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Session(models.Model):
    course = models.ForeignKey('Course')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    counselor = models.ForeignKey('mbu.Counselor')
    #teaching_assistants = models.ManyToManyField(User)
    #merit_badge_university = models.ForeignKey('MeritBadgeUniversity')
