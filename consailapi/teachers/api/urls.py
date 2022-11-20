from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from consailapi.consultations.api.views import ConsultationStudentViewSet
from consailapi.teachers.api.views import LessonViewSet, TeacherViewSet

router = DefaultRouter()

router.register("teachers", TeacherViewSet, basename="teachers")
nested_router = routers.NestedSimpleRouter(router, r"teachers", lookup="teacher")
nested_router.register("lessons", LessonViewSet, basename="lesson-view-set")
nested_router.register(
    "consultations",
    ConsultationStudentViewSet,
    basename="consultation-student-view-set",
)
urlpatterns = [
    path("", include(nested_router.urls), name=""),
] + router.urls
