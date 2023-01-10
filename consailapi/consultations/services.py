from copy import deepcopy
from datetime import timedelta
from typing import Any
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError as RestValidationError

from consailapi.consultations.models import Consultation, Reservation, ReservationSlot
from consailapi.students.models import Student
from consailapi.teachers.models import Teacher
from consailapi.users.helpers import send_email_task
from consailapi.users.models import User


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

        previous_student = None
        student = None

        for slot in self.consultation.slots.all():
            if slot.reservation:
                student = slot.reservation.student
                slot.reservation.is_cancelled = True
                slot.reservation.save()

            if student and student != previous_student:
                send_email_task.delay(
                    user_uuid=slot.reservation.student.uuid,
                    temp_content={
                        "message": f"{slot.reservation.teacher.get_full_name()} just cancel your reservation"
                    },
                )
                previous_student = student

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
            uuids = ReservationSlot.objects.filter(
                start_time__gte=start_time, start_time__lt=end_time
            ).values_list("uuid", flat=True)
            free_slots_data.append(
                {"start_time": start_time, "end_time": end_time, "uuids": uuids}
            )
        return free_slots_data


class ReservationService:
    def __init__(self, reservation: Reservation | None = None):
        self.reservation = reservation

    def cancel_reservation(self, user: User) -> Reservation:
        if not self.reservation:
            raise ValueError("Missing reservation")

        self.reservation.is_cancelled = True
        self.reservation.save()
        self.reservation.slots.update(reservation=None)
        send_email_task.delay(
            user_uuid=user.uuid,
            temp_content={
                "message": f"Reservation has been canceled {self.reservation.slots.all()}"
            },
        )

        return self.reservation

    @transaction.atomic
    def create_reservation(
        self, consultation: Consultation, student: Student, **reservation_data: Any
    ) -> Reservation:
        if consultation.start_time < timezone.now() + timedelta(hours=1):
            raise RestValidationError(
                "It is too late to create a reservation for this consultation"
            )

        uuids = reservation_data.get("uuids")
        slots = consultation.slots.filter(uuid__in=uuids).order_by("start_time")
        if slots.filter(reservation__isnull=False).exists():
            raise RestValidationError("Consultation slots are not free")
        reservation = Reservation(
            teacher=consultation.teacher,
            student=student,
            start_time=slots.first().start_time,
            end_time=slots.last().start_time + timedelta(minutes=15),
        )
        try:
            reservation.full_clean()
            reservation.save()
            self.reservation = reservation

        except ValidationError as e:
            raise RestValidationError(e.messages)
        slots.update(reservation=reservation)

        send_email_task.delay(
            user_uuid=consultation.teacher.uuid,
            temp_content={
                "message": f"{student.get_full_name()} just make "
                f"reservation to {reservation.slots.objects.first().start_time}"
            },
        )
        return reservation

    @transaction.atomic
    def make_absent(self) -> Reservation:
        if not self.reservation:
            raise ValueError("Missing reservation")

        self.reservation.was_absent = True
        self.reservation.save()
        return self.reservation
