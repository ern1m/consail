from typing import Any

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from consailapi.chats.api.serializers import (
    CreateThreadSerializer,
    MessageSerializer,
    ThreadSerializer,
)
from consailapi.chats.models import Message, Thread
from consailapi.chats.services import MessageService, ThreadService
from consailapi.students.models import Student
from consailapi.teachers.consts import ResponseMessages
from consailapi.teachers.models import Teacher
from consailapi.users.consts import UserType


class ThreadViewSet(ModelViewSet):
    queryset = Thread.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    serializer_class = ThreadSerializer

    def get_queryset(self) -> QuerySet[Thread]:
        user: Teacher | Student = self.request.user  # noqa

        if user.user_type == UserType.TEACHER.label:
            return (
                self.queryset.filter(teacher=user)
                .select_related("teacher", "student")
                .prefetch_related("student__messages", "teacher__messages")
            )
        elif user.user_type == UserType.STUDENT.label:
            return (
                self.queryset.filter(student=user)
                .select_related("teacher", "student")
                .prefetch_related("student__messages", "teacher__messages")
            )

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data
        serializer = CreateThreadSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = ThreadService().create(serializer.validated_data)
        serializer = self.get_serializer(obj)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class MessagesViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    queryset = Message.objects.all().select_related("sender")
    permission_classes = (IsAuthenticated,)
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    search_fields = [
        "content",
    ]
    ordering_fields = [
        "id",
        "created_at",
    ]

    def get_queryset(self, *args, **kwargs) -> QuerySet[Message]:
        thread_uuid = self.kwargs.get("thread_uuid")
        try:
            thread = Thread.objects.get(uuid=thread_uuid)
        except Thread.DoesNotExist:
            raise NotFound(ResponseMessages.THREAD_NOT_FOUND)
        return self.queryset.filter(thread=thread)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        sender: Teacher | Student = request.user  # noqa
        thread_uuid = self.kwargs.get("thread_uuid")

        try:
            thread = Thread.objects.get(uuid=thread_uuid)
        except Thread.DoesNotExist:
            raise NotFound(ResponseMessages.THREAD_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = MessageService().create(
            sender=sender, thread=thread, message_data=serializer.validated_data
        )
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
