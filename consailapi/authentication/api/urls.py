from django.urls import path

from consailapi.authentication.api.views import login, logout

app_name = "auth"
urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
]
