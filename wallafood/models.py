from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    location = models.CharField(max_length=30, blank=True)
    photo_url = models.CharField(max_length=255, blank=True)
    contact = models.TextField(max_length=11, blank=True)
    preferences = models.TextField(max_length=500, blank=True)


class Advert(models.Model):
    id_advert = models.IntegerField(default=0)
    name = models.CharField(max_length=200, null=False)
    vendor = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=500, null=False)
    amount_available = models.IntegerField()
    allergens =  models.CharField(max_length=200, null=False)
    vote_average = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    status = models.CharField(max_length=20)
    photo_url = models.CharField(max_length=300, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)