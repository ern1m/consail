from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class UserType(TextChoices):
    TEACHER = "TEACHER", _("Teacher")
    STUDENT = "STUDENT", _("Student")
