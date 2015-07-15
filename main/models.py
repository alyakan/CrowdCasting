from django.db import models
from django.contrib.auth.models import User


class Actor(models.Model):
    user = models.OneToOneField(User)


class HeadShots(models.Model):
    user = models.ForeignKey(Actor)
    image = models.ImageField(
        upload_to='actors/head_shots/',
        blank=True,
        null=True)


class Trial(models.Model):
    user = models.ForeignKey(Actor)
    name = models.CharField(max_length=100)


class Experience(models.Model):
    experience = models.CharField(max_length=200)
    actor = models.ForeignKey(Actor, related_name='experiences')

    def __unicode__(self):
        return unicode(self.experience)


class ProfilePicture(models.Model):
    actor = models.OneToOneField(Actor)
    profile_picture = models.ImageField(
        upload_to='actors/profile_pictures/',
        blank=True,
        null=True)
