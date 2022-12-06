from django.urls import include, path

urlpatterns = [
    path("", include("consailapi.users.api.urls")),
    path("", include("consailapi.teachers.api.urls")),
    path("", include("consailapi.students.api.urls")),
    path("", include("consailapi.school.api.urls")),
    path("", include("consailapi.lessons.api.urls")),
    path("", include("consailapi.consultations.api.urls")),
    path("", include("consailapi.chats.api.urls")),
]
