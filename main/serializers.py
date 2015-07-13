from rest_framework import serializers
from main.models import Actor, Experience


class ActorSeriealizer(serializers.HyperlinkedModelSerializer):
    experiences = serializers.StringRelatedField(many=True)

    class Meta:
        model = Actor
        fields = ('experiences')


class ExperienceSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField('actor.username')

    class Meta:
        model = Experience
        fields = ('actor, experience')
