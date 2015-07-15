from main.models import Actor, Experience, ContactInfo
from rest_framework import viewsets, permissions
from main.serializers import (
    ActorSerializer, ExperienceSerializer, ContactInfoSerializer)
from main.permissions import IsOwnerOrReadOnly


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


class ContactInfoViewSet(viewsets.ModelViewSet):
    """
    creates a viewset for the contactinfo models
    author: Nourhan
    """
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(actor=Actor.objects.get(id=self.request.user.id))
