from django.db import models
from django.utils.translation import gettext_lazy as _

from consailapi.shared.models import BaseModel


class Department(BaseModel):
    name = models.CharField(_("Department name"), blank=True, max_length=100)

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return self.name


class Major(BaseModel):
    name = models.CharField(_("Major"), blank=True, max_length=100)
    department = models.ForeignKey(
        Department,
        null=True,
        verbose_name=_("Major Department"),
        on_delete=models.SET_NULL,
        related_name="major",
    )

    class Meta:
        verbose_name = _("Major")
        verbose_name_plural = _("Majors")

    def __str__(self):
        return self.name
