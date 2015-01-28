from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Scout(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateTimeField()
    rank = models.CharField(max_length=15)
    troop = models.CharField(max_length=15)
