from django.urls import include, path
from rest_framework.routers import DefaultRouter

from consailapi.school.api.views import MajorView

router = DefaultRouter()

router.register("majors", MajorView, basename="majors-view-set")

urlpatterns = [
    path("", include(router.urls), name="major-view-sets"),
]
