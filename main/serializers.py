from rest_framework import serializers
from main.models import (
    Actor, Experience,
    RequestContactInfo,
    Tag,
    Education)

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password', 'id', 'is_staff')
        # write_only_fields = ('password',)
        read_only_fields = (
            'is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def create(self, attrs):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user = super(UserSerializer, self).create(attrs)
        user.set_password(attrs['password'])
        user.save()
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
            'id', 'url', 'first_name', 'middle_name', 'last_name', 'date_of_birth',
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


class RequestContactInfoSerializer(
        serializers.HyperlinkedModelSerializer):

    """
    serializes the request contact info model data
    author: Nourhan
    """
    director = serializers.ReadOnlyField(source='user.id')
    actor = serializers.HyperlinkedIdentityField(
        view_name='actor-detail', source='actor_id')
    status = serializers.ReadOnlyField()

    class Meta:
        model = RequestContactInfo
        fields = ['url', 'actor', 'director', 'actor_id', 'status']
