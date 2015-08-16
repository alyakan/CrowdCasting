from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Actor(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50)


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


class RequestAccountNotification(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=100, blank=False)


class RequestContactInfo(models.Model):
    sender = models.ForeignKey(User, related_name='requestcontactinfo')
    actor_username = models.CharField(max_length=100)


class ContactInfo(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], blank=False, max_length=100)
    actor = models.ForeignKey(Actor, related_name='contactinfo')

    def __unicode__(self):
        return unicode(self.phone_number)


class Tag(models.Model):
    """
    Represents a single tag for an actor
    Author: Aly Yakan
    """
    actor = models.ForeignKey(Actor)

    tag = models.CharField(max_length=128)
