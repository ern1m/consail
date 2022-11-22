from copy import deepcopy
from datetime import timedelta
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.exceptions import ValidationError as RestValidationError

from consailapi.consultations.models import Consultation, Reservation, ReservationSlot
from consailapi.students.models import Student
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
            try:
                slot.full_clean()
                slot.save()
                slot_start_time += timedelta(minutes=15)
            except ValidationError as e:
                raise RestValidationError(e.messages)


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
    def create_multiple(
        self, teacher: Teacher, consultation_data: dict
    ) -> [Consultation]:
        data = deepcopy(consultation_data)
        consultations = []
        for i in range(0, 5):
            data["start_time"] = consultation_data["start_time"] + timedelta(weeks=i)
            data["end_time"] = consultation_data["end_time"] + timedelta(weeks=i)
            consultation = Consultation(teacher=teacher, **data)
            try:
                consultation.full_clean()
                consultation.save()
            except ValidationError as e:
                raise RestValidationError(e.messages)

            ReservationSlotService().create_for_consultation(consultation=consultation)
            consultations.append(consultation)

        return consultations

    @transaction.atomic
    def delete(self) -> None:
        if not self.consultation:
            raise ValueError("Missing consultation")

        for slot in self.consultation.slots.all():
            if slot.reservation:
                slot.reservation.is_cancelled = True
                slot.reservation.save()
        self.consultation.delete()

    @transaction.atomic
    def delete_multiple(self, teacher: Teacher, uuids: [UUID]) -> None:
        for reservation in Consultation.objects.filter(
            teacher=teacher, uuid__in=uuids, slots__reservation__isnull=False
        ):
            reservation.is_cancelled = True
            reservation.save()
        Consultation.objects.filter(teacher=teacher, uuid__in=uuids).delete()

    @transaction.atomic
    def update_hours(self, consultation_data: dict) -> Consultation:
        if not self.consultation:
            raise ValueError("Missing consultation")
        for slot in self.consultation.slots.all():
            if slot.reservation:
                slot.reservation.is_cancelled = True
                slot.reservation.save()
            slot.delete()
        for attr, value in consultation_data.items():
            setattr(self.consultation, attr, value)
        try:
            self.consultation.full_clean()
            self.consultation.save()
        except ValidationError as e:
            raise RestValidationError(e.messages)
        ReservationSlotService().create_for_consultation(consultation=self.consultation)
        return self.consultation

    def get_available_slots(self, duration: timedelta) -> list:
        if not self.consultation:
            raise ValueError("Missing consultation")
        free_slots = self.consultation.slots.all().filter(reservation__isnull=True)
        free_slots_data = []
        for slot in free_slots:
            start_time = slot.start_time
            end_time = start_time + duration
            if start_time + duration > self.consultation.end_time:
                break
            if (
                self.consultation.slots.all()
                .filter(
                    start_time__gte=start_time,
                    start_time__lt=end_time,
                    reservation__isnull=False,
                )
                .exists()
            ):
                continue
            free_slots_data.append({"start_time": start_time, "end_time": end_time})
        return free_slots_data


class ReservationService:
    def __init__(self, reservation: Reservation | None = None):
        self.reservation = reservation

    def cancel_reservation(self) -> Reservation:
        if not self.reservation:
            raise ValueError("Missing reservation")
        self.reservation.is_cancelled = True
        self.reservation.save()
        self.reservation.slots.update(reservation=None)
        return self.reservation

    @transaction.atomic
    def create_reservation(
        self, consultation: Consultation, student: Student, **reservation_data
    ) -> Reservation:
        start_time = reservation_data.get("start_time")
        end_time = reservation_data.get("end_time")
        slots = consultation.slots.filter(
            start_time__gte=start_time, start_time__lte=end_time - timedelta(minutes=15)
        )
        if slots.filter(reservation__isnull=False).exists():
            raise ValueError("Consultation slots are not free")
        reservation = Reservation(
            teacher=consultation.teacher,
            student=student,
            start_time=start_time,
            end_time=end_time,
        )
        try:
            reservation.full_clean()
            reservation.save()
            self.reservation = reservation
        except ValidationError as e:
            raise RestValidationError(e.messages)
        slots.update(reservation=reservation)
        return reservation
