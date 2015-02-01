from django.db import models
from django.contrib.auth.models import User
from troop.models import Troop

# Create your models here.

class Scoutmaster(models.Model):
    user = models.OneToOneField(User)
    troop = models.ForeignKey(Troop)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return "%d - %s %s" % (self.pk, self.user.first_name, self.user.last_name)
