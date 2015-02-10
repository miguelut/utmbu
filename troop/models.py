from django.db import models
from django.contrib.auth.models import User
from mbu.models import Address

# Create your models here.

class Council(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name',)

class Troop(models.Model):
    number = models.CharField(max_length=10)
    council = models.ForeignKey(Council)

    def __str__(self):
        return "%s - %s" % (self.number, self.council)

    class Meta:
        unique_together = ('number','council')


class TroopContact(models.Model):
    user = models.OneToOneField(User)
    address = models.ForeignKey(Address)
    troop = models.ForeignKey(Troop)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return "%s %s %s" % (self.user.first_name, self.user.last_name, self.phone_number)
