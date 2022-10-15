from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from consailapi.teachers.models import Teacher
from consailapi.users.admin import UserAdmin


@admin.register(Teacher)
class TeacherAdmin(UserAdmin):
    list_display = ["email", "__str__", "uuid", "created_at"]
    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            _("Personal info"),
            {"fields": ("degrees", "first_name", "last_name", "name_display", "email")},
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
