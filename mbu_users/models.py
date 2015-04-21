from django.db import models
from django.contrib.auth.models import User
from troop.models import Troop
from mbu.models import Address

# Create your models here.
class Counselor(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=12)

class Venture(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateTimeField()

class Volunteer(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateTimeField()

class TroopContact(models.Model):
    user = models.OneToOneField(User)
    address = models.ForeignKey(Address)
    troop = models.ForeignKey(Troop)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return "%s %s %s" % (self.user.first_name, self.user.last_name, self.phone_number)

class Parent(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=12)
    troop = models.ForeignKey(Troop)

    def __str__(self):
        return "%d - %s %s" % (self.pk, self.user.first_name, self.user.last_name)
    
    class Meta:
       permissions = (
           ('can_edit_scout_schedule', "Can edit own scouts' schedules.")
       )
