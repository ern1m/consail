from django.db import models
from django.utils.translation import gettext_lazy as _

from consailapi.school.models import Major
from consailapi.shared.consts import WeekDays
from consailapi.shared.helpers import get_time_formatted
from consailapi.shared.models import BaseModel
from consailapi.teachers.models import Teacher


class Subject(BaseModel):
    name = models.CharField(_("name"), blank=False, max_length=200)
    major = models.ForeignKey(
        Major,
        verbose_name=_("major"),
        related_name=_("subjects"),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self) -> str:
        return _(f"{self.name} - {self.major}")


class Lesson(BaseModel):
    subject = models.ForeignKey(
        Subject,
        verbose_name=_("subject"),
        related_name=_("lessons"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    teacher = models.ForeignKey(
        Teacher,
        verbose_name=_("teacher"),
        related_name=_("lessons"),
        null=True,
        on_delete=models.SET_NULL,
    )
    day = models.CharField(
        _("day"),
        max_length=20,
        choices=WeekDays.choices,
        null=False,
        blank=False,
    )
    start_time = models.TimeField(_("start time"), blank=False, null=False)
    end_time = models.TimeField(_("end time"), blank=False, null=False)
    room = models.CharField(_("room"), max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")

    def __str__(self):
        return _(f"{self.subject}")

    @property
    def start_time_display(self) -> str:
        return get_time_formatted(self.start_time)

    @property
    def end_time_display(self) -> str:
        return get_time_formatted(self.end_time)

    @property
    def full_date(self) -> str:
        return _(f"{self.day} {self.start_time}-{self.end_time}")
