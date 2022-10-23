from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from consailapi.teachers.api.serializers import (
    TeacherDetailSerializer,
    TeacherListSerializer,
)
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
