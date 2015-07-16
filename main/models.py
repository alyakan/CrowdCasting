from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Actor(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(
        upload_to='actors/profile_pictures/',
        blank=True,
        null=True)
    name = models.CharField(max_length=100)


class HeadShots(models.Model):
    # user = models.ForeignKey(Actor)
    image = models.ImageField(
        upload_to='actors/head_shots/',
        blank=True,
        null=True)


class Trial(models.Model):
    name = models.CharField(max_length=100)


class Experience(models.Model):
    experience = models.CharField(max_length=200)
    actor = models.ForeignKey(Actor, related_name='experiences')

    def __unicode__(self):
        return unicode(self.experience)


class RequestAccountNotification(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)


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
