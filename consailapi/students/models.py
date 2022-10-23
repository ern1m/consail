from django.db import models
from django.utils.translation import gettext_lazy as _

from consailapi.school.models import Major
from consailapi.users.models import User


class Student(User):
    year = models.PositiveSmallIntegerField(_("Year of study"), default=0)
    major = models.ForeignKey(
        Major,
        null=True,
        verbose_name=_("Students Major"),
        on_delete=models.SET_NULL,
        related_name="students",
    )

    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")

    def __str__(self):
        return self.email
