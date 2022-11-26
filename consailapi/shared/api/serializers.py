from rest_framework import serializers


class UuidSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()


class UuidListSerializer(serializers.Serializer):
    uuids = serializers.ListField(child=serializers.UUIDField())
