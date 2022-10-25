from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from consailapi.school.api.serializers import MajorSerializer
from consailapi.students.models import Student
from consailapi.users.api.serializers import UserSerializer


class RegisterStudentSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    repeat_password = serializers.CharField(required=True)

    def validate_password(self, password: str):
        validate_password(password)
        return password


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


class StudentDetailSerializer(serializers.ModelSerializer):
    major = MajorSerializer()

    class Meta:
        model = Student
        lookup_field = "uuid"
        fields = [
            "first_name",
            "last_name",
            "year",
            "major",
            "email",
            "uuid",
        ]
