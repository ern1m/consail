from django.contrib import admin

# Register your models here.
from consailapi.consultations.models import Consultation, ReservationType


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ["teacher", "uuid", "__str__"]
    readonly_fields = [
        "uuid",
    ]
    list_select_related = [
        "teacher",
    ]


@admin.register(ReservationType)
class ReservationTypeAdmin(admin.ModelAdmin):
    readonly_fields = [
        "uuid",
    ]
    list_select_related = [
        "teacher",
    ]
