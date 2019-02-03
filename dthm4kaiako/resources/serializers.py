from rest_framework import serializers
from resources.models import Resource


class ResourceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        """Meta settings for serializer."""

        model = Resource
        fields = ('id', 'name', 'slug', 'datetime_added', 'datetime_updated')
