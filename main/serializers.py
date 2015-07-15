from rest_framework import serializers
from main.models import HeadShots, Trial
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
            'username', 'password', 'first_name', 'last_name', 'email',)
        write_only_fields = ('password',)
        read_only_fields = (
            'is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def create(self, attrs):
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        user = super(UserSerializer, self).create(attrs)
        user.set_password(attrs['password'])
        return user
