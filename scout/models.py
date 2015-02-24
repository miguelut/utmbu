from django.db import models
from django.contrib.auth.models import User
from troop.models import Troop

# Create your models here.

class Scout(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateField()
    rank = models.CharField(max_length=15)
    troop = models.ForeignKey(Troop)
    numClasses = models.IntegerField()

    def __str__(self):
        return "%d - %s %s" % (self.pk, self.user.first_name, self.user.last_name)

    class Meta:
        permissions = (
            ('edit_scout_schedule','Can edit schedule'),
        )
