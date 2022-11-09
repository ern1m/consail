from django.contrib import admin

from consailapi.consultation.models import Consultation, Reservation, ReservationType


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    pass


@admin.register(ReservationType)
class ReservationTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass
