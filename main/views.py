
from main.models import (
    Actor, Experience,
    ContactInfo, HeadShots,
    Trial, RequestAccountNotification,
    RequestContactInfo)
from rest_framework import viewsets, permissions
from rest_framework import serializers
from main.serializers import(
    HeadShotsSerializer,
    TrialSerializer,
    UserSerializer,
    ActorSerializer,
    ExperienceSerializer,
    RequestAccountNotificationSerializer,
    ContactInfoSerializer,
    RequestContactInfoSerializer,
)
from main import permissions as myPermissions
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    # allow non-authenticated user to create via POST
    #     return (permissions.AllowAny() if self.request.method == 'POST'
    #             else myPermissions.IsStaffOrTargetUser()),


class HeadShotsViewSet(viewsets.ViewSet):
    queryset = HeadShots.objects.all()

    def list(self, request):
        queryset = HeadShots.objects.all()
        serializer = HeadShotsSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        listOfThings = request.DATA['images']

        serializer = HeadShotsSerializer(
            data=listOfThings, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @detail_route(methods=['get'])
    def retrieve(self, request, pk=None):
        queryset = HeadShots.objects.all()
        image = get_object_or_404(queryset, pk=pk)
        serializer = HeadShotsSerializer(image)
        return Response(serializer.data)

# class HeadShotsViewSet(viewsets.ModelViewSet):
#     queryset = HeadShots.objects.all()
#     serializer_class = HeadShotsSerializer


class TrialViewSet(viewsets.ViewSet):
    queryset = Trial.objects.all()

    def list(self, request):
        queryset = Trial.objects.all()
        serializer = TrialSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        listOfThings = request.DATA['names']

        serializer = TrialSerializer(
            data=listOfThings, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Actor.objects.all()
        elif self.request.user.is_authenticated():
            return Actor.objects.filter(
                id=Actor.objects.get(
                    user_id=self.request.user.id).id)
        else:
            return Actor.objects.none()


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = (
        permissions.IsAuthenticated, myPermissions.IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(actor=Actor.objects.get(id=self.request.user.id))

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Experience.objects.all()
        elif self.request.user.is_authenticated():
            return Experience.objects.filter(
                actor_id=Actor.objects.get(
                    user_id=self.request.user.id))
        else:
            return Experience.objects.none()


class RequestAccountViewSet(viewsets.ModelViewSet):
    queryset = RequestAccountNotification.objects.all()
    serializer_class = RequestAccountNotificationSerializer
    permission_classes = (myPermissions.IsSuperUserOrTargetUser,)

    def get_queryset(self):
        if self.request.user and self.request.user.is_superuser:
            return RequestAccountNotification.objects.all()
        else:
            return RequestAccountNotification.objects.none()


class RequestContactInfoViewSet(viewsets.ModelViewSet):
    queryset = RequestContactInfo.objects.all()
    serializer_class = RequestContactInfoSerializer
    permission_classes = (
        permissions.IsAuthenticated, myPermissions.IsStaffOrTargetUser)

    def get_queryset(self):
        if self.request.user and self.request.user.is_superuser:
            return RequestContactInfo.objects.filter(sender=self.request.user)
        else:
            return

    def perform_create(self, serializer):
        users = User.objects.all()
        requests = RequestContactInfo.objects.all()
        actor_username = self.request.data['actor_username']

        for r in requests:
            if ((r.sender == self.request.user) and
               (r.actor_username == actor_username)):
                raise serializers.ValidationError(
                    'You have already sent a request to this actor.')
            else:
                if self.request.user.username == actor_username:
                    raise serializers.ValidationError(
                        'You cannot send a request to yourself.')
                else:
                    user = User.objects.get(username=actor_username)
                    if user.is_staff:
                        raise serializers.ValidationError(
                            'You cannot send a request to another director.')

        for u in users:
            if u.username == actor_username:
                serializer.save(sender=self.request.user)
                return
        raise serializers.ValidationError(
                'This username is invalid. Please try again.')


class ContactInfoViewSet(viewsets.ModelViewSet):
    """
    This is a list of all phone numbers for the currently signed in user
    author: Nourhan
    """
    serializer_class = ContactInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'

    def get_queryset(self):
        """
        This view should return the contact info
        for the currently authenticated user.
        """
        return ContactInfo.objects.filter(
            actor=Actor.objects.get(user=self.request.user))

    def perform_create(self, serializer):
        queryset = ContactInfo.objects.filter(
            actor=Actor.objects.get(user=self.request.user))

        if queryset.count() > 0:
            raise serializers.ValidationError(
                'You are only allowed to post one phone number.')
        else:
            serializer.save(actor=Actor.objects.get(user=self.request.user))
