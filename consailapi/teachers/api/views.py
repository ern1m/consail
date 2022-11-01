from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from consailapi.lessons.api.serializers import LessonBaseSerializer
from consailapi.lessons.models import Lesson
from consailapi.teachers.api.serializers import (
    TeacherDetailSerializer,
    TeacherListSerializer,
)
from consailapi.teachers.consts import ResponseMessages
from consailapi.teachers.models import Teacher
from consailapi.users.api.serializers import UserSerializer


class TeacherViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = Teacher.objects.all().filter(is_active=True)
    lookup_field = "uuid"

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action == "list":
            return TeacherListSerializer
        if self.action == "retrieve":
            return TeacherDetailSerializer


class LessonViewSet(GenericViewSet, ListModelMixin):
    serializer_class = LessonBaseSerializer
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
            raise NotFound(ResponseMessages.TEACHER_NOT_FOUND)
        return self.queryset.filter(teacher=teacher)
