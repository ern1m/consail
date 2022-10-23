from rest_framework.routers import DefaultRouter

from consailapi.teachers.api.views import TeacherViewSet

router = DefaultRouter()

router.register("teachers", TeacherViewSet, basename="teachers")

urlpatterns = [] + router.urls
