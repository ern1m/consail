from django.urls import path

from consailapi.authentication.api.views import login

app_name = "auth"
urlpatterns = [path("login/", login)]
