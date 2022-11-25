from django.urls import include, path
from rest_framework.routers import DefaultRouter

from consailapi.consultations.api.views import ConsultationViewSet, ReservationViewSet

router = DefaultRouter()

router.register("consultations", ConsultationViewSet, basename="consultation-view-set")
router.register("reservation", ReservationViewSet, basename="student-reservation")

urlpatterns = [
    path("", include(router.urls), name="consultation-view-sets"),
]
