from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated

from consailapi.lessons.api.serializers import LessonListSerializer, SubjectSerializer
from consailapi.lessons.models import Lesson, Subject
from consailapi.teachers.models import Teacher


class SubjectViewSet(viewsets.GenericViewSet, ListModelMixin):
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = Subject.objects.all().select_related("major")
    permission_classes = (IsAuthenticated,)
    search_fields = ["name", "major__name", "major__department__name"]
    ordering_fields = [
        "id",
        "name",
    ]


class LessonViewSet(viewsets.GenericViewSet, ListModelMixin):
    serializer_class = LessonListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = Lesson.objects.all().select_related("teacher", "subject")
    permission_classes = (IsAuthenticated,)
    lookup_field = "uuid"
    search_fields = [
        "subject__name",
    ]
    ordering_fields = [
        "id",
    ]

    def get_queryset(self, *args, **kwargs) -> QuerySet[Lesson]:
        teacher_uuid = self.kwargs.get("teacher_uuid")
        try:
            teacher = Teacher.objects.get(uuid=teacher_uuid)
        except Teacher.DoesNotExist:
            raise NotFound("aaa")
        return self.queryset.filter(teacher=teacher)
