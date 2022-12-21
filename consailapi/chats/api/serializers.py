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
    teacher = UserSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    messages = MessageSerializer(many=True, required=False)

    class Meta:
        model = Thread
        fields = [
            "uuid",
            "teacher",
            "student",
            "messages",
        ]


class CreateThreadSerializer(serializers.Serializer):
    teacher_uuid = serializers.UUIDField()
    student_uuid = serializers.UUIDField()
