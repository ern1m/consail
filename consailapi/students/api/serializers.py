# from django.conf import settings
from rest_framework import serializers

from consailapi.students.models import Student
from consailapi.users.api.serializers import UserSerializer


class RegisterStudentSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True
    )  # validators=[x.items for x in settings.AUTH_PASSWORD_VALIDATORS])
    repeat_password = serializers.CharField(required=True)


class StudentSerializer(UserSerializer):
    username = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(write_only=True)

    class Meta:
        model = Student
        fields = [
            *UserSerializer.Meta.fields,
            "username",
            "password",
            "is_active",
        ]
