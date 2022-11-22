from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsTeacherPermission(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        return True if user.is_authenticated and hasattr(user, "teacher") else False


class IsStudentPermission(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        return True if user.is_authenticated and hasattr(user, "student") else False
