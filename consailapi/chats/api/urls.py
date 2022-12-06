from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from consailapi.chats.api.views import MessagesViewSet, ThreadViewSet

router = DefaultRouter()


router.register("threads", ThreadViewSet, basename="consultation-view-set")
nested_router = routers.NestedSimpleRouter(router, r"threads", lookup="thread")
nested_router.register("messages", MessagesViewSet, basename="messages-view-set")

urlpatterns = [
    path("", include(router.urls), name="chats-view-sets"),
    path("", include(nested_router.urls), name="messages-view-sets"),
]
