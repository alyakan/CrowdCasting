from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Actor(models.Model):
    user = models.OneToOneField(User)


class Experience(models.Model):
    experience = models.CharField(max_length=200)
    actor = models.ForeignKey(Actor, related_name='experiences')

    def __unicode__(self):
        return unicode(self.experience)


class ContactInfo(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], blank=True, max_length=100)
    actor = models.ForeignKey(Actor, related_name='ContactInfo')

    def __unicode__(self):
        return unicode(self.phone_number)
