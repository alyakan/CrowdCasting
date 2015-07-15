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
        serializer.save(actor=Actor.objects.get(user=self.request.user))
