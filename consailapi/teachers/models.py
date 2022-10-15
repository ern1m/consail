from django.db import models
from django.utils.translation import gettext_lazy as _

from consailapi.users.models import User


class Teacher(User):
    degrees = models.CharField(_("degrees"), max_length=50, null=True, blank=True)
    name_display = models.CharField(
        _("name display"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            "Leave this blank if you want the default way of showing the name (degrees, first name, last name)"
        ),
    )

    class Meta:
        verbose_name = _("teacher")
        verbose_name_plural = _("teachers")

    def __str__(self) -> str:
        name_display = self.name_display.strip() if self.name_display else None
        return name_display or self.get_name_display or self.email

    @property
    def get_name_display(self) -> str:
        return f"{self.degrees or ''} {self.get_full_name() or ''}".strip()
