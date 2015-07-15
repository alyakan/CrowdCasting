from django.db import models
from django.contrib.auth.models import User


class Actor(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(
        upload_to='actors/profile_pictures/',
        blank=True,
        null=True)


class HeadShots(models.Model):
    # user = models.ForeignKey(Actor)
    image = models.ImageField(
        upload_to='actors/head_shots/',
        blank=True,
        null=True)


class Trial(models.Model):
    name = models.CharField(max_length=100)
