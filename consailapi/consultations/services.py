from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.exceptions import ValidationError as RestValidationError

from consailapi.consultations.models import Consultation, ReservationSlot
from consailapi.teachers.models import Teacher


class ReservationSlotService:
    def __init__(self, reservation_slot: ReservationSlot | None = None):
        self.reservation_slot = reservation_slot

    def create_for_consultation(self, consultation: Consultation) -> None:
        slot_start_time = consultation.start_time
        while slot_start_time <= consultation.end_time - timedelta(minutes=15):
            slot = ReservationSlot(
                reservation=None, consultation=consultation, start_time=slot_start_time
            )
            slot.full_clean()
            slot.save()
            slot_start_time += timedelta(minutes=15)


class ConsultationService:
    def __init__(self, consultation: Consultation | None = None):
        self.consultation = consultation

    @transaction.atomic
    def create(self, teacher: Teacher, consultation_data: dict) -> Consultation:
        consultation = Consultation(teacher=teacher, **consultation_data)
        try:
            consultation.full_clean()
            consultation.save()
        except ValidationError as e:
            raise RestValidationError(e.messages)
        ReservationSlotService().create_for_consultation(consultation=consultation)
        self.consultation = consultation
        return consultation

    @transaction.atomic
    def delete(self) -> None:
        if not self.consultation:
            raise ValueError("Missing consultation")

        for slot in self.consultation.slots.all():
            if slot.reservation:
                slot.reservation.is_cancelled = True
                slot.reservation.save()
        self.consultation.delete()
