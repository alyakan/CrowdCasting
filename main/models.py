from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]


class Actor(models.Model):
    """
    Represents an instance of an actor.
    Author: Aly Yakan
    """
    user = models.OneToOneField(User)

    first_name = models.CharField(max_length=256, null=True)
    middle_name = models.CharField(max_length=256, null=True)
    last_name = models.CharField(max_length=256, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(choices=GENDER_CHOICES,
                              default='',
                              blank=True,
                              max_length=128,
                              null=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    hair_color = models.CharField(max_length=256, null=True)
    eye_color = models.CharField(max_length=256, null=True)
    skin_color = models.CharField(max_length=256, null=True)
    about_me = models.CharField(max_length=1024, null=True)
    full_body_shot = models.ImageField(
        upload_to='actors/full_body_shots/',
        blank=True,
        null=True)
    profile_picture = models.ImageField(
        upload_to='actors/profile_pictures/',
        blank=True,
        null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], blank=False, max_length=100)


class Experience(models.Model):
    experience = models.CharField(max_length=200)
    actor = models.ForeignKey(Actor, related_name='experiences')

    def __unicode__(self):
        return unicode(self.experience)


class RequestContactInfo(models.Model):
    director = models.ForeignKey(User, related_name='requestcontactinfo')

    actor_id = models.IntegerField()


class Tag(models.Model):
    """
    Represents a single tag for an actor
    Author: Aly Yakan
    """
    actor = models.ForeignKey(Actor, related_name='tags')

    tag = models.CharField(max_length=128)


class Education(models.Model):

    actor = models.ForeignKey(Actor, related_name='education')
    year = models.IntegerField()
    qualification = models.CharField(max_length=128)
    where = models.CharField(max_length=128)
