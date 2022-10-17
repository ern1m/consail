from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.request import Request

from consailapi.authentication.consts import AuthenticationMessage
from consailapi.users.models import User


class AuthenticationService:
    def authenticate(self, login_data: dict, request: Request) -> User:
        email = login_data.get("email")
        password = login_data.get("password")

        if email and password:
            user = authenticate(request, email=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    AuthenticationMessage.INVALID_CREDENTIALS
                )
        else:
            raise serializers.ValidationError(AuthenticationMessage.MISSING_DATA)

        return user  # noqa

    def create_token(self, login_data: dict, request: Request) -> Token:
        user = self.authenticate(login_data=login_data, request=request)
        token, created = Token.objects.get_or_create(user=user)
        return token
