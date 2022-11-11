from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from consailapi.shared.helpers import get_time_formatted
from consailapi.shared.models import BaseModel
from consailapi.teachers.models import Teacher


class Consultation(BaseModel):
    start_time = models.DateTimeField(_("start time"), null=False, blank=False)
    end_time = models.DateTimeField(_("end time"), null=False, blank=False)
    teacher = models.ForeignKey(
        Teacher,
        verbose_name=_("teacher"),
        on_delete=models.CASCADE,
        related_name="consultations",
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = _("Consultation")
        verbose_name_plural = _("Consultations")

    def __str__(self) -> str:
        return f"{self.start_time.date()}: {get_time_formatted(self.start_time)}-{get_time_formatted(self.end_time)}"

    def clean(self) -> None:
        if self.start_time >= self.end_time:
            raise ValidationError(_("Start time can't be greater than end time"))
        if (
            self.start_time
            and self.end_time
            and Consultation.objects.filter(teacher=self.teacher)
            .exclude(id=self.id)
            .filter(
                Q(
                    (
                        Q(start_time__lt=self.end_time)
                        & Q(start_time__gt=self.start_time)
                    )
                    | (Q(end_time__lt=self.end_time) & Q(end_time__gt=self.start_time))
                    | Q(start_time__lte=self.start_time, end_time__gte=self.end_time)
                )
            )
            .exists()
        ):
            raise ValidationError(
                _("Teacher can't have more than one consultation at the same time")
            )
