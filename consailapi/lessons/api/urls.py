from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from consailapi.lessons.api.views import LessonViewSet, SubjectViewSet
from consailapi.teachers.api.urls import router as teachers_router

router = DefaultRouter()

router.register("subjects", SubjectViewSet, basename="subject-view-set")

nested_router = routers.NestedSimpleRouter(
    teachers_router, r"teachers", lookup="teacher"
)
nested_router.register("lessons", LessonViewSet, basename="lesson-view-set")
# router.register()

urlpatterns = [
    path("schedule/", include(router.urls), name=""),
    path("", include(nested_router.urls), name=""),
]
