from typing import Any

from django.conf import settings
from django.utils.datetime_safe import datetime
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from consailapi.authentication.api.serializers import LoginSerializer
from consailapi.authentication.consts import AuthenticationMessage
from consailapi.authentication.services import AuthenticationService
from consailapi.students.api.serializers import (
    AuthorizeSerializer,
    RegisterStudentSerializer,
    StudentSerializer,
)
from consailapi.students.models import Student
from consailapi.students.services import StudentService
from consailapi.users.api.serializers import UserSerializer
from consailapi.users.helpers import send_email_task
from consailapi.users.models import User


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = AuthenticationService().create_token(
            serializer.validated_data, self.request
        )

        return Response({"token": token.key})


login = LoginView.as_view()


class RegisterViewSet(
    GenericViewSet,
):
    permission_classes = (AllowAny,)
    queryset = Student.objects.all()
    serializer_class = RegisterStudentSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        ss = StudentService()
        request_body = RegisterStudentSerializer(data=request.data)
        request_body.is_valid(raise_exception=True)

        data = ss.prepare_student_data(request_body.data)

        obj = StudentSerializer(data=data)
        obj.is_valid(raise_exception=True)
        obj.save()

        user = User.objects.filter(email=obj.data.get("email")).first()
        user.register_token = User.generate_key()
        user.save()

        send_email_task.delay(
            user_uuid=user.uuid,
            temp_content={
                "message": f"Click <a href='{settings.FRONTEND_URL}"
                f"/verify-email/?token={user.register_token}'>here</a> "
                f"to confirm your account"
            },
        )
        return Response(status=status.HTTP_201_CREATED, data=obj.data)

    @extend_schema(request=AuthorizeSerializer)
    @action(methods=["POST"], detail=False)
    def authorize(self, request, *args, **kwargs):
        serializer = AuthorizeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(**serializer.validated_data)
        except User.DoesNotExist:
            raise ValidationError("User not found")

        user.register_token = None
        user.email_verified_at = datetime.now()
        user.save()

        return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        AuthenticationService().destroy_token(user=request.user)
        return Response({"message": AuthenticationMessage.LOGOUT_SUCCESSFUL})


logout = LogoutView.as_view()
