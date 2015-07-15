from rest_framework import serializers
from main.models import Actor, Experience, ContactInfo


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


class ContactInfoSerializer(serializers.HyperlinkedModelSerializer):
    """
    serializes the contact info model data
    author: Nourhan
    """
    actor = serializers.ReadOnlyField(source='actor.id')

    class Meta:
        model = ContactInfo
        fields = ('url', 'actor', 'phone_number')
