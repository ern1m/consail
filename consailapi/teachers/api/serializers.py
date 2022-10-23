from rest_framework import serializers

from consailapi.teachers.models import Teacher


class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["get_name_display", "email", "uuid"]


class TeacherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        lookup_field = "uuid"
        fields = [
            "first_name",
            "last_name",
            "degrees",
            "name_display",
            "get_name_display",
            "email",
            "uuid",
        ]
