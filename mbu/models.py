from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Scout(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateTimeField()
    rank = models.CharField(max_length=15)
    # troop = models.ForeignKey('Troop')
    troop = models.CharField(max_length=15)
    
class Troop(models.Model):
    council = models.CharField(max_length=100)

class TroopContact(models.Model):
    user = models.OneToOneField(User)
    address = models.ForeignKey('Address')
    phone_number = models.CharField(max_length=12)

class Address(models.Model):
    street_address = models.CharField(max_length=200)
    street_address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)

class Counselor(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=12)


class Venture(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateTimeField()

#This class will represent the yearly MBU so we can 
#retain inforamation across multiple years
class MeritBadgeUniversity(models.Model):
    year = models.DateTimeField()

class WaitingList(models.Model):
    scout = models.ForeignKey('Scout')
    course = models.ForeignKey('course.Course')
    position_in_line = models.IntegerField()
