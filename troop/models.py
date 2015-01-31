from django.db import models
from django.contrib.auth.models import User
from mbu.models import Address

# Create your models here.

class Council(models.Model):
    name = models.CharField(max_length=100)

class Troop(models.Model):
    number = models.CharField(max_length=10)
    council = models.ForeignKey(Council)

class TroopContact(models.Model):
    user = models.OneToOneField(User)
    address = models.ForeignKey(Address)
    troop = models.ForeignKey(Troop)
    phone_number = models.CharField(max_length=12)

