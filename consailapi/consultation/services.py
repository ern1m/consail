from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as RestValidationError

from consailapi.consultation.models import Reservation, ReservationType


class ReservationService:
    def __init__(self, reservation: Reservation | None = None):
        self.reservation = reservation

    def create(
        self, reservation_data: dict, reservation_type: ReservationType
    ) -> Reservation:
        try:
            reservation = Reservation.objects.get()
        except Reservation.DoesNotExist:
            reservation = Reservation(
                **reservation_data,
                duration=reservation_type.duration,
                name=reservation_type.name,
            )

        try:
            reservation.full_clean()
            reservation.save()

            self.reservation = reservation
        except ValidationError as e:
            raise RestValidationError(e.messages)
        return self.reservation
