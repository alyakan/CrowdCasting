from main.models import Actor, Experience, Biography
from rest_framework import viewsets, permissions
from main.serializers import (
    ActorSerializer, ExperienceSerializer, BiographySerializer)
from main.permissions import IsOwnerOrReadOnly, CanPostBio


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(actor=Actor.objects.get(id=self.request.user.id))


class BiographyViewSet(viewsets.ModelViewSet):

    """
    Author: Kareem Tarek .
    """
    queryset = Biography.objects.all()
    serializer_class = BiographySerializer
    permission_classes = (
        permissions.IsAuthenticated, IsOwnerOrReadOnly, CanPostBio)

    def perform_create(self, serializer):
        serializer.save(actor=Actor.objects.get(id=self.request.user.id))
