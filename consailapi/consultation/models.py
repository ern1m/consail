from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from consailapi.lessons.models import Subject
from consailapi.shared.models import BaseModel
from consailapi.teachers.models import Teacher


class Consultation(BaseModel):
    day = models.DateField(_("Consultation Day"))
    start_time = models.DateTimeField(_("Consultation start time"))
    end_time = models.DateTimeField(_("Consultation start time"))
    teacher = models.ForeignKey(
        Teacher,
        verbose_name=_("Teacher"),
        on_delete=models.CASCADE,
        related_name="consultations",
    )

    class Meta:
        verbose_name = _("Consultation")
        verbose_name_plural = _("Consultations")

    def __str__(self):
        return f"{self.day}: {self.start_time} - {self.end_time}"


class ReservationType(BaseModel):
    name = models.CharField(_("Consultation name"), max_length=150)
    teacher = models.ForeignKey(
        Teacher,
        verbose_name=_("Teacher"),
        on_delete=models.CASCADE,
        related_name="reservation_type",
    )
    duration = models.DurationField(_("Duration"), help_text="HH:MM:SS")

    class Meta:
        verbose_name = _("Reservation type")
        verbose_name_plural = _("Reservation types")

    def __str__(self):
        return self.name


class Reservation(BaseModel):
    start_time = models.DateTimeField(_("Reservation start time"))
    type = models.ForeignKey(
        ReservationType,
        verbose_name=_("Consultation type"),
        on_delete=models.SET_NULL,
        related_name="students",
        null=True,
        blank=True,
    )
    consultation = models.ForeignKey(
        Consultation,
        verbose_name=_("Reservation"),
        on_delete=models.DO_NOTHING,
        related_name="reservation",
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name=_("Subject"),
        related_name="reservation",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    duration = models.DurationField(
        _("Copy of ReservationType duration"), help_text="HH:MM:SS"
    )
    name = models.CharField(_("Copy of ReservationType name"), max_length=150)

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")

    def __str__(self):
        return self.start_time

    @property
    def end_time(self):
        return self.start_time + self.duration

    def clean(self) -> None:
        if self.start_time >= self.end_time:
            raise ValidationError(_("Start time can't be greater than end time"))

        if (
            self.start_time
            and self.end_time
            and (
                self.start_time >= self.consultation.end_time
                or self.end_time <= self.consultation.start_time
            )
        ):
            raise ValidationError(
                _("Teacher can't have more than one lesson at the same time")
            )
