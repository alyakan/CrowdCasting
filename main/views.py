
from main.models import (
    Actor, Experience,
    ContactInfo, HeadShots,
    Trial, RequestAccountNotification,
    RequestContactInfo,
    ProfilePicture,
    Tag, Education)
from rest_framework import viewsets, permissions
from rest_framework import serializers
from main.serializers import(
    HeadShotsSerializer,
    TrialSerializer,
    UserSerializer,
    ActorSerializer,
    ExperienceSerializer,
    ProfilePictureSerializer,
    RequestAccountNotificationSerializer,
    ContactInfoSerializer,
    RequestContactInfoSerializer,
    TagSerializer,
    EducationSerializer

)
from main import permissions as myPermissions
from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (myPermissions.UserIsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)

    # def get_permissions(self):
    # allow non-authenticated user to create via POST
    #     return (permissions.AllowAny() if self.request.method == 'POST'
    #             else myPermissions.IsStaffOrTargetUser()),

    def perform_create(self, serializer):
        password = serializer.data['password']
        username = serializer.data['username']
        user = serializer.save()
        Actor.objects.create(
            user=user)
        user = authenticate(
            username=username,
            password=password)
        login(self.request, user)


class DirectorViewSet(UserViewSet):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id, is_staff=True)

    def perform_create(self, serializer):
        password = serializer.data['password']
        username = serializer.data['username']
        user = serializer.save()
        user.is_staff = True
        user.save()
        user = authenticate(
            username=username,
            password=password)
        login(self.request, user)


class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        myPermissions.UpdateOnly)

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Actor.objects.all()
        elif self.request.user.is_authenticated():
            try:
                return Actor.objects.filter(
                    id=Actor.objects.get(
                        user_id=self.request.user.id).id)
            except:
                return Actor.objects.none()
        else:
            return Actor.objects.none()


class RequestContactInfoViewSet(viewsets.ModelViewSet):
    queryset = RequestContactInfo.objects.all()
    serializer_class = RequestContactInfoSerializer
    permission_classes = (
        permissions.IsAuthenticated, myPermissions.IsStaffOrTargetUser,
        myPermissions.PreventUpdate)

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return RequestContactInfo.objects.filter(sender=self.request.user)
        else:
            return

    def perform_create(self, serializer):
        requests = RequestContactInfo.objects.all()
        actor_username = self.request.data['actor_username']
        users = User.objects.all()

        for r in requests:
            if ((r.sender == self.request.user) and
               (r.actor_username == actor_username)):
                raise serializers.ValidationError(
                    'You have already sent a request to this actor.')
        if self.request.user.username == actor_username:
            raise serializers.ValidationError(
                        'You cannot send a request to yourself.')
        try:
            user = User.objects.get(username=actor_username)
        except:
            raise serializers.ValidationError(
                            'This username is invalid. Please try again.')
        if user.is_staff:
            print "sdaads"
            raise serializers.ValidationError(
                'You cannot send a request to another director.')

        for u in users:
            if u.username == actor_username:
                serializer.save(sender=self.request.user)
                return
        raise serializers.ValidationError(
                            'This username is invalid. Please try again.')