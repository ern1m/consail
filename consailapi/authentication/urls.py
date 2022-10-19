from django.urls import path

from consailapi.authentication.api.views import login, logout

app_name = "auth"

urlpatterns = [path("login/", login), path("logout/", logout)]
