from typing import Any

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from consailapi.authentication.api.serializers import LoginSerializer
from consailapi.authentication.consts import AuthenticationMessage
from consailapi.authentication.services import AuthenticationService
from consailapi.students.api.serializers import (
    RegisterStudentSerializer,
    StudentSerializer,
)
from consailapi.students.models import Student
from consailapi.students.services import StudentService
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

        send_email_task.delay(
            user=user.uuid,
            temp_content={
                "message": "Click <a href='https://consail.site'>here</a> to confirm account"
            },
        )
        return Response(status=status.HTTP_201_CREATED, data=obj.data)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        AuthenticationService().destroy_token(user=request.user)
        return Response({"message": AuthenticationMessage.LOGOUT_SUCCESSFUL})


logout = LogoutView.as_view()
