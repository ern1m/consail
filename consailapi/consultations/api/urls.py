from django.urls import include, path
from rest_framework.routers import DefaultRouter

from consailapi.consultations.api.views import ConsultationViewSet

router = DefaultRouter()

router.register("consultations", ConsultationViewSet, basename="consultation-view-set")

urlpatterns = [
    path("", include(router.urls), name="consultation-view-sets"),
]
