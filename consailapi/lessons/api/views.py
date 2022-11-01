from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from consailapi.lessons.api.serializers import (
    LessonActionSerializer,
    LessonBaseSerializer,
    SubjectSerializer,
)
from consailapi.lessons.models import Lesson, Subject
from consailapi.lessons.services import LessonService
from consailapi.users.permissions import IsTeacherPermission


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


class LessonViewSet(viewsets.GenericViewSet, CreateModelMixin):
    serializer_class = LessonActionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = Lesson.objects.all().select_related("teacher", "subject")
    permission_classes = (IsTeacherPermission,)
    lookup_field = "uuid"
    search_fields = [
        "subject__name",
    ]
    ordering_fields = [
        "id",
    ]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        teacher = request.user.teacher  # noqa
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lesson = LessonService().create(serializer.validated_data, teacher=teacher)
        return Response(
            LessonBaseSerializer(lesson).data, status=status.HTTP_201_CREATED
        )
