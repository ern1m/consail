from rest_framework import serializers

from consailapi.chats.models import Message, Thread
from consailapi.users.api.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "uuid",
            "sender",
            "content",
            "created_at",
        ]
        lookup_field = "uuid"


class ThreadSerializer(serializers.ModelSerializer):
    teacher = serializers.UUIDField(source="teacher.uuid")
    student = serializers.UUIDField(source="student.uuid")
    messages = MessageSerializer(many=True)

    class Meta:
        model = Thread
        fields = [
            "uuid",
            "teacher",
            "student",
            "messages",
        ]
