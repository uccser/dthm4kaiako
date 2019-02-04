from rest_framework import serializers
from resources.models import Resource, ResourceComponent


class ResourceComponentSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta settings for serializer."""

        model = ResourceComponent
        fields = (
            'name',
            'component_type',
            'component_url',
            'component_file',
            'component_resource',
        )


class ResourceSerializer(serializers.ModelSerializer):

    components = ResourceComponentSerializer(many=True, read_only=True)

    class Meta:
        """Meta settings for serializer."""

        model = Resource
        fields = (
            'id',
            'name',
            'slug',
            'datetime_added',
            'datetime_updated',
            'components'
        )
