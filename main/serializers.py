from rest_framework import serializers
from main.models import (
    Actor, Experience,
    ContactInfo, HeadShots,
    Trial, RequestAccountNotification,
    RequestContactInfo,
    ProfilePicture,
    Tag)

from django.contrib.auth.models import User
from drf_haystack.serializers import HaystackSerializer
from .search_indexes import ActorIndex


class HeadShotsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HeadShots
        fields = ('image',)


class TrialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trial
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'password', 'first_name', 'last_name', 'email',)
        # write_only_fields = ('password',)
        read_only_fields = (
            'is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def create(self, attrs):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        print attrs
        user = super(UserSerializer, self).create(attrs)
        user.set_password(attrs['password'])
        user.save()
        Actor.objects.create(
            user_id=user.id,
            name=user.first_name+" "+user.last_name)
        return user


class ActorSerializer(serializers.HyperlinkedModelSerializer):

    # experiences = serializers.StringRelatedField(many=True)
    # profile_picture = serializers.HyperlinkedRelatedField(
    #     many=True, view_name='experience-detail', read_only=True)

    experiences = serializers.HyperlinkedRelatedField(
        many=True, view_name='experience-detail', read_only=True)
    contactinfo = serializers.HyperlinkedRelatedField(
        many=True, view_name='contactinfo-detail', read_only=True)

    class Meta:
        model = Actor
        fields = ('url', 'name', 'experiences', 'contactinfo')


class ExperienceSerializer(serializers.HyperlinkedModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.id')

    class Meta:
        model = Experience
        fields = ('url', 'actor', 'experience')


class ProfilePictureSerializer(serializers.HyperlinkedModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.id')

    class Meta:
        model = ProfilePicture
        fields = ('url', 'actor', 'profile_picture',)


class RequestAccountNotificationSerializer(
        serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RequestAccountNotification
        fields = ['name', 'phone_number']


class ContactInfoSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializes the contact info model data
    author: Nourhan
    """
    actor = serializers.ReadOnlyField(source='actor.id')

    class Meta:
        model = ContactInfo
        fields = ('url', 'actor', 'phone_number')


class RequestContactInfoSerializer(
        serializers.HyperlinkedModelSerializer):
    """
    serializes the request contact info model data
    author: Nourhan
    """
    sender = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = RequestContactInfo
        fields = ['url', 'sender', 'actor_username']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the Tag model data
    Author: Aly Yakan
    """
    actor = serializers.ReadOnlyField(source='actor.name')

    class Meta:
        model = Tag
        fields = ['url', 'tag', 'actor']


class ActorSearchSerializer(HaystackSerializer):

    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [ActorIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = [
            "text", "name", 
        ]

