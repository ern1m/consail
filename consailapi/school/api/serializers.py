from rest_framework import serializers

from consailapi.school.models import Department, Major


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "uuid",
            "name",
        ]


class MajorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Major
        fields = [
            "uuid",
            "name",
            "department",
        ]
