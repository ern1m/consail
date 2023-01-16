from rest_framework.permissions import BasePermission


class IsTeacherPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user
        return True if user.is_authenticated and hasattr(user, "teacher") else False


class IsStudentPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user
        return True if user.is_authenticated and hasattr(user, "student") else False


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view) -> bool:
        user = request.user
        return (
            True if user.is_authenticated and user.email_verified_at else False  # noqa
        )
