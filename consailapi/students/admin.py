from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from consailapi.students.models import Student
from consailapi.users.admin import UserAdmin


@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ["email", "__str__", "uuid", "created_at"]
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "created_at", "updated_at")},
        ),
    )
    search_fields = ["last_name", "email"]
    readonly_fields = ["updated_at", "created_at"]
