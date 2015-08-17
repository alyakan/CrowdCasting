
from main.models import (
    Actor,
    RequestContactInfo)
from rest_framework import viewsets, permissions
from rest_framework import serializers
from main.serializers import(
    UserSerializer,
    ActorSerializer,
    RequestContactInfoSerializer,

)
from main import permissions as myPermissions
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
            return RequestContactInfo.objects.filter(
                director=self.request.user)
        else:
            return

    def perform_create(self, serializer):
        requests = RequestContactInfo.objects.all()
        actor_id = self.request.data['actor_id']
        actors = Actor.objects.all()

        for r in requests:
            if ((r.director == self.request.user) and
               (r.actor_id == actor_id)):
                raise serializers.ValidationError(
                    'You have already sent a request to this actor.')
        # if self.request.user == actor:
        #     raise serializers.ValidationError(
        #                 'You cannot send a request to yourself.')
        try:
            actor = Actor.objects.get(id=actor_id)
        except:
            raise serializers.ValidationError(
                            'Invalid actor. Please try again.')
        # if user.is_staff:
        #     print "sdaads"
        #     raise serializers.ValidationError(
        #         'You cannot send a request to another director.')

        for a in actors:
            if a.id == actor.id:
                serializer.save(director=self.request.user)
                return
        raise serializers.ValidationError(
                            'Invalid actor. Please try again.')
