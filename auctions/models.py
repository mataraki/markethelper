from datetime import datetime  
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import DecimalField
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    price = models.DecimalField(max_digits=16, decimal_places=2, default='0')
    photo = models.URLField(max_length=256, blank=True)
    category = models.CharField(max_length=64, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchings")
    isopen = models.BooleanField(default=True)
    winner = models.CharField(max_length=64, blank=True)

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=16, decimal_places=2, default='0')
    bidcount = models.IntegerField(default='0')

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    text = models.CharField(max_length=256, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)