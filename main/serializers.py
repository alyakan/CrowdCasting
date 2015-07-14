from rest_framework import serializers
from main.models import Actor, Experience


class ActorSerializer(serializers.HyperlinkedModelSerializer):
    # experiences = serializers.StringRelatedField(many=True)
    experiences = serializers.HyperlinkedRelatedField(
        many=True, view_name='experience-detail', read_only=True)

    class Meta:
        model = Actor
        fields = ('url', 'experiences')


class ExperienceSerializer(serializers.HyperlinkedModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.id')

    class Meta:
        model = Experience
        fields = ('url', 'actor', 'experience')
