from django.urls import include, path
from rest_framework.routers import DefaultRouter

from consailapi.authentication.api.views import RegisterViewSet

router = DefaultRouter()


router.register("register", RegisterViewSet, basename="student-register-view-set")

urlpatterns = [
    path("", include(router.urls), name="student-register"),
]
