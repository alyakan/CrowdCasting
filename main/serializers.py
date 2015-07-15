from rest_framework import serializers
from main.models import Actor, Experience, Biography


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


class BiographySerializer(serializers.HyperlinkedModelSerializer):

    """
    Serializer for Biography model.
    Author: Kareem Tarek .
    """
    actor = serializers.ReadOnlyField(source='actor.id')

    class Meta:
        model = Biography
        fields = ('url', 'actor', 'date_of_birth',
                  'family_information', 'personal_life', 'place_of_birth')
