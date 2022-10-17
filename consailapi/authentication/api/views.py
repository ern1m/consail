from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from consailapi.authentication.api.serializers import LoginSerializer
from consailapi.authentication.consts import AuthenticationMessage
from consailapi.authentication.services import AuthenticationService


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


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        AuthenticationService().destroy_token(user=request.user)
        return Response({"message": AuthenticationMessage.LOGOUT_SUCCESSFUL})


logout = LogoutView.as_view()
