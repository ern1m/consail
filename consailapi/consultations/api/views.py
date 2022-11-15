from typing import Any

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from consailapi.consultations.api.serializers import (
    ConsultationDetailSerializer,
    ConsultationSimpleActionSerializer,
)
from consailapi.consultations.models import Consultation
from consailapi.consultations.services import ConsultationService
from consailapi.users.permissions import IsTeacherPermission


class ConsultationViewSet(ModelViewSet):
    queryset = Consultation.objects.all().select_related("teacher")
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    permission_classes = (IsTeacherPermission,)

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action in ["create", "update", "partial_update", "list"]:
            return ConsultationSimpleActionSerializer
        else:
            return ConsultationDetailSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Endpoint for creating a single consultation. It can be created by teacher.
        """
        teacher = self.request.user.teacher  # noqa
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ConsultationService().create(
            teacher=teacher, consultation_data=serializer.validated_data
        )
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Endpoint for deleting a single consultation. It can be deleted by teacher.
        """
        consultation = self.get_object()
        ConsultationService(consultation).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Endpoint for updating start time and end time of a single consultation. It can be updated by teacher.
        After the teacher updates the consultation hours, all the reservations for the consultation are cancelled.
        Students must create a reservation once again.
        """
        partial = kwargs.pop("partial", False)
        consultation = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        ConsultationService(consultation).update_hours(
            consultation_data=serializer.validated_data
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)
