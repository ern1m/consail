from django.contrib import admin

from consailapi.school.models import Department, Major


class MajorInLine(admin.TabularInline):
    readonly_fields = ("uuid",)
    model = Major
    extra = 0


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = (MajorInLine,)
    readonly_fields = ("uuid",)
