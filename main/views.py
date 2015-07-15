
from main.models import Actor, Experience, ContactInfo, HeadShots, Trial
from rest_framework import viewsets, permissions
from rest_framework import serializers
from main.serializers import(
    HeadShotsSerializer,
    TrialSerializer,
    UserSerializer,
    ActorSerializer,
    ExperienceSerializer,
    ContactInfoSerializer
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
    #     # allow non-authenticated user to create via POST
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
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (
        permissions.IsAuthenticated, myPermissions.IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(actor=Actor.objects.get(user=self.request.user))


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
