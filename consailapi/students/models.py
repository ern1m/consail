from django.utils.translation import gettext_lazy as _

from consailapi.users.models import User


class Student(User):
    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")

    def __str__(self):
        return self.email
