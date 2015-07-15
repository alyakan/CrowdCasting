from rest_framework import serializers
from main.models import HeadShots, Trial
from django.contrib.auth.models import User
from main.models import Actor, Experience, RequestAccountNotification


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
        write_only_fields = ('password',)
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
    experiences = serializers.HyperlinkedRelatedField(
        many=True, view_name='experience-detail', read_only=True)

    class Meta:
        model = Actor
        fields = ('url', 'name', 'experiences')


class ExperienceSerializer(serializers.HyperlinkedModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.id')

    class Meta:
        model = Experience
        fields = ('url', 'actor', 'experience')


class RequestAccountNotificationSerializer(
        serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RequestAccountNotification
        fields = ['name', 'email']
