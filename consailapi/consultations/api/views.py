from datetime import timedelta
from typing import Any

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from consailapi.consultations.api.serializers import (
    ConsultationDetailSerializer,
    ConsultationSimpleActionSerializer,
    ReservationDurationSerializer,
    ReservationSerializer,
    ReservationTimeSerializer,
    ReservationUuidSerializer,
)
from consailapi.consultations.models import Consultation, Reservation
from consailapi.consultations.services import ConsultationService, ReservationService
from consailapi.users.permissions import IsTeacherPermission


class ConsultationViewSet(ModelViewSet):
    queryset = Consultation.objects.all().select_related("teacher")
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    permission_classes = (IsTeacherPermission,)

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action in [
            "create",
            "update",
            "partial_update",
            "list",
            "create_for_a_month_forward",
        ]:
            return ConsultationSimpleActionSerializer
        elif self.action == "cancel_reservation":
            return ReservationUuidSerializer
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

    @action(
        detail=True,
        methods=[
            "POST",
        ],
        url_path="cancel-reservation",
    )
    def cancel_reservation(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        consultation = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            uuid = serializer.validated_data.get("reservation_uuid")
            reservation = consultation.reservations.filter(
                is_cancelled=False, uuid=uuid
            ).first()
        except Reservation.DoesNotExist:
            raise NotFound("Missing reservation")
        reservation = ReservationService(reservation).cancel_reservation()
        return Response(
            ReservationSerializer(reservation).data, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["POST"], url_path="create-multiple")
    def create_for_a_month_forward(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        teacher = self.request.user.teacher  # noqa
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        consultations = ConsultationService().create_multiple(
            teacher=teacher, consultation_data=serializer.validated_data
        )
        response_data = self.get_serializer(consultations, many=True).data
        return Response(response_data, status=status.HTTP_201_CREATED)


class ConsultationStudentViewSet(GenericViewSet, ListModelMixin):
    queryset = Consultation.objects.all().select_related("teacher")
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    permission_classes = (IsAuthenticated,)
    serializer_class = ConsultationSimpleActionSerializer

    def get_queryset(self):
        uuid = self.kwargs.get("teacher_uuid")
        return self.queryset.filter(teacher__uuid=uuid).all()

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action == "get_available_slots":
            return ReservationDurationSerializer
        return ConsultationSimpleActionSerializer

    @action(
        methods=["POST"],
        url_path="get-available-slots",
        detail=True,
    )
    def get_available_slots(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        consultation = self.get_object()
        duration = timedelta(minutes=serializer.validated_data.get("duration"))
        available_slots = ConsultationService(consultation).get_available_slots(
            duration
        )
        return Response(
            ReservationTimeSerializer(available_slots, many=True).data,
            status=status.HTTP_200_OK,
        )
