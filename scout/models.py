from django.db import models
from django.contrib.auth.models import User
from troop.models import Troop

# Create your models here.

class Scout(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateTimeField()
    rank = models.CharField(max_length=15)
    troop = models.ForeignKey(Troop)
