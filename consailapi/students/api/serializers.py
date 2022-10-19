from rest_framework import serializers

from consailapi.students.models import Student
from consailapi.users.api.serializers import UserSerializer


class RegisterStudentSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    repeat_password = serializers.CharField(required=True)


class StudentSerializer(UserSerializer):
    is_active = serializers.BooleanField(write_only=True)

    class Meta:
        model = Student
        fields = [
            *UserSerializer.Meta.fields,
            "password",
            "is_active",
        ]
