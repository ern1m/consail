from django.contrib import admin

from consailapi.lessons.models import Lesson, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    list_display = ("name", "major", "uuid")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    list_display = (
        "subject",
        "uuid",
        "start_time_display",
        "end_time_display",
        "day",
        "teacher",
    )
