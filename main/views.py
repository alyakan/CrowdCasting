from main.models import Actor, Experience
from rest_framework import viewsets
from main.serializers import ActorSeriealizer, ExperienceSerializer


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSeriealizer


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
