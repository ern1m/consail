from rest_framework.exceptions import ValidationError

from consailapi.students.models import Student
from consailapi.users.admin import User


class StudentService:
    def __init__(self, student: Student | None = None):
        self.student = student

    def prepare_student_data(self, post_data: dict | None) -> dict:
        if not post_data:
            raise
        if (
            post_data.get("email")
            and User.objects.filter(email=post_data.get("email")).exists()
        ):
            raise ValidationError("User with this mail already exist")

        if (
            post_data.get("password") and post_data.get("repeat_password")
        ) and post_data.get("password") != post_data.get("repeat_password"):
            raise ValidationError("Password are not the same")

        post_data.pop("repeat_password")
        post_data["username"] = post_data["email"]
        post_data["is_active"] = False
        return post_data
