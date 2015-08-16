from rest_framework import serializers
from main.models import (
    Actor, Experience,
    ContactInfo, HeadShots,
    Trial, RequestAccountNotification,
    RequestContactInfo,
    ProfilePicture,
    Tag,
    Education)

from django.contrib.auth.models import User


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
            'username', 'first_name', 'last_name', 'email', 'password')
        # write_only_fields = ('password',)
        read_only_fields = (
            'is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def create(self, attrs):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user = super(UserSerializer, self).create(attrs)
        user.set_password(attrs['password'])
        user.save()
        Actor.objects.create(
            user_id=user.id)
        return user


class TagSerializer(serializers.ModelSerializer):

    """
    Serializes the Tag model data
    Author: Aly Yakan
    """

    class Meta:
        model = Tag
        fields = ['id', 'tag']


class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = ('id', 'experience',)


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = ('id', 'qualification',)


class ActorSerializer(serializers.HyperlinkedModelSerializer):

    # experiences = serializers.StringRelatedField(many=True)
    # profile_picture = serializers.HyperlinkedRelatedField(
    #     many=True, view_name='experience-detail', read_only=True)

    experiences = ExperienceSerializer(many=True)
    tags = TagSerializer(many=True)
    education = EducationSerializer(many=True)
    # contactinfo = serializers.HyperlinkedRelatedField(
    #     many=True, view_name='contactinfo-detail', read_only=True)

    class Meta:
        model = Actor
        fields = (
            'url', 'first_name', 'middle_name', 'last_name', 'date_of_birth',
            'gender', 'height', 'weight', 'hair_color', 'eye_color',
            'skin_color', 'about_me', 'full_body_shot', 'profile_picture',
            'experiences', 'phone_number', 'education', 'tags',
        )

    def create(self, validated_data):
        experiences = validated_data.pop('experiences')
        tags = validated_data.pop('tags')
        education = validated_data.pop('education')

        actor = Actor.objects.create(
            user=self.context['request'].user,
            **validated_data)
        for experience in experiences:
            Experience.objects.create(actor=actor, **experience)
        for tag in tags:
            Tag.objects.create(actor=actor, **tag)
        for edu in education:
            Education.objects.create(actor=actor, **education)
        return actor

    def update(self, instance, validated_data):
        experiences = validated_data.pop('experiences')
        tags = validated_data.pop('tags')
        educations = validated_data.pop('education')
        actor = Actor.objects.get(
            id=instance.id, user=self.context['request'].user)
        actor = Actor(
            id=instance.id,
            user=self.context['request'].user,
            **validated_data)
        actor.save()

        Experience.objects.filter(actor=instance).delete()
        for item in experiences:
            experience = Experience(
                experience=item['experience'],
                actor=instance)
            experience.save()

        Tag.objects.filter(actor=instance).delete()
        for item in tags:
            tag = Tag(tag=item['tag'], actor=instance)
            tag.save()

        Education.objects.filter(actor=instance).delete()
        for item in educations:
            education = Education(
                year=item['year'],
                qualification=item['qualification'],
                where=item['where'])
            education.save()
        return instance


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
