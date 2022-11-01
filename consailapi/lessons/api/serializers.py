from rest_framework import serializers

from consailapi.lessons.models import Lesson, Subject
from consailapi.school.api.serializers import MajorSerializer


class SubjectSerializer(serializers.ModelSerializer):
    major = MajorSerializer()

    class Meta:
        model = Subject
        fields = ["uuid", "name", "major"]


class LessonBaseSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Lesson
        fields = [
            "uuid",
            "subject",
            "day",
            "start_time_display",
            "end_time_display",
            "room",
        ]


class LessonActionSerializer(serializers.ModelSerializer):
    subject_uuid = serializers.UUIDField()

    class Meta:
        model = Lesson
        fields = [
            "uuid",
            "subject_uuid",
            "day",
            "start_time",
            "end_time",
            "room",
        ]
