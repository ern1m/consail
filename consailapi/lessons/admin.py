from django.contrib import admin

from consailapi.lessons.models import Lesson, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
