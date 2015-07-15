from django.db import models
from django.contrib.auth.models import User


class Actor(models.Model):
    user = models.OneToOneField(User)


class Experience(models.Model):
    experience = models.CharField(max_length=200)
    actor = models.ForeignKey(Actor, related_name='experiences')

    def __unicode__(self):
        return unicode(self.experience)


class Biography(models.Model):

    """
    A Single Biography entry
    Author: Kareem Tarek .
    """
    date_of_birth = models.DateField()
    family_information = models.CharField(max_length=200)
    personal_life = models.CharField(max_length=200)
    place_of_birth = models.CharField(max_length=200)
    actor = models.OneToOneField(Actor, related_name='biography')
