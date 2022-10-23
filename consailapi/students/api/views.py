from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from consailapi.students.api.serializers import StudentDetailSerializer
from consailapi.students.models import Student
from consailapi.users.permissions import IsTeacherPermission


class StudentViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = StudentDetailSerializer
    queryset = Student.objects.all().filter(is_active=True)
    lookup_field = "uuid"
    permission_classes = (IsTeacherPermission,)
