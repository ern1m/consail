from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class WeekDays(TextChoices):
    MON = "MONDAY", _("Monday")
    TUE = "TUESDAY", _("Tuesday")
    WED = "WEDNESDAY", _("Wednesday")
    THU = "THURSDAY", _("Thursday")
    FRI = "FRIDAY", _("Friday")
    SAT = "SATURDAY", _("Saturday")
    SUN = "SUNDAY", _("Sunday")
