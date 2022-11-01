from django.urls import include, path
from rest_framework.routers import DefaultRouter

from consailapi.lessons.api.views import LessonViewSet, SubjectViewSet

router = DefaultRouter()

router.register("subjects", SubjectViewSet, basename="subject-view-set")
router.register("lessons", LessonViewSet, basename="lesson-view-set")


urlpatterns = [
    path("schedule/", include(router.urls), name=""),
]
