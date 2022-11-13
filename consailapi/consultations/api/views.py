from typing import Any

from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from consailapi.consultations.api.serializers import ConsultationSimpleActionSerializer
from consailapi.consultations.models import Consultation
from consailapi.consultations.services import ConsultationService
from consailapi.users.permissions import IsTeacherPermission


class ConsultationViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    queryset = Consultation.objects.all().select_related("teacher")
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    permission_classes = (IsTeacherPermission,)

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action in [
            "create",
        ]:
            return ConsultationSimpleActionSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        teacher = self.request.user.teacher  # noqa
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ConsultationService().create(
            teacher=teacher, consultation_data=serializer.validated_data
        )
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        consultation = self.get_object()
        ConsultationService(consultation).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
