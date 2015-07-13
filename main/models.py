from django.db import models
from django.contrib.auth.models import User


class Actor(models.Model):
    user = models.OneToOneField(User)


class Experience(models.Model):
    experience = models.CharField(max_length=200)
    actor = models.ForeignKey(Actor, related_name='experiences')
