from django.urls import path
from rest_framework.routers import DefaultRouter

from consailapi.authentication.api.views import RegisterViewSet, login, logout

router = DefaultRouter()

app_name = "auth"
router.register("register", RegisterViewSet, basename="student-register-view-set")
urlpatterns = [path("login/", login), path("logout/", logout)] + router.urls
