from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    user_type = serializers.CharField(required=False, read_only=True)
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "uuid", "user_type"]
        lookup_field = "uuid"
