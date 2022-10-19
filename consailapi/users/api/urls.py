from django.urls import include, path
from rest_framework.routers import DefaultRouter

from consailapi.users.api.views import UserViewSet

router = DefaultRouter()

router.register("users", UserViewSet, basename="users-view-set")

urlpatterns = [
    path("", include(router.urls), name="users-view-sets"),
]
