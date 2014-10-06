from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200)

class Session(models.Model):
    #start time
    #end time
    #teacher
    #course
    teaching_assistants = models.ManyToManyField(User)

class Scout(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateTimeField()
    rank = models.CharField(max_length=15)
    troop = models.ForeignKey(Troop)
    pass
    
class Troop(models.Model):
    council = models.CharField(max_length=100)

class TroopContact(models.Model):
    user = models.OneToOneField(User)
    address = models.ForeignKey(Address)
    pass

class Address(models.Model):
    street_address = models.CharField(max_length=200)
    street_address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    pass

class Counselor(models.Model):
    user = models.OneToOneField(User)
    pass

class Venture(models.Model):
    user = models.OneToOneField(User)
    dob = models.DateTimeField()
    pass

#This class will represent the yearly MBU so we can 
#retain inforamation across multiple years
class MeritBadgeUniversity(models.Model):
    year = models.DateTimeField()
    pass

class WaitingList(models.Model):
    #scout
    #class
    #position in line
    pass
