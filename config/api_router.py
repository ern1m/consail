from django.urls import include, path

urlpatterns = [
    path("", include("consailapi.users.api.urls")),
    path("", include("consailapi.authentication.api.urls")),
]
