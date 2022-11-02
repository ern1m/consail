from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError as RestValidationError

from consailapi.lessons.models import Lesson, Subject
from consailapi.teachers.models import Teacher


class LessonService:
    def __init__(self, lesson: Lesson | None = None):
        self.lesson = lesson

    def create(self, lesson_data: dict, teacher: Teacher) -> Lesson:
        subject_uuid = lesson_data.pop("subject_uuid", None)
        try:
            subject = Subject.objects.get(uuid=subject_uuid)
        except Subject.DoesNotExist:
            raise NotFound("Missing subject")
        lesson = Lesson(teacher=teacher, subject=subject, **lesson_data)
        try:
            lesson.full_clean()
            lesson.save()
            self.lesson = lesson
        except ValidationError as e:
            raise RestValidationError(e.messages)
        return self.lesson

    def delete(self) -> None:
        if not self.lesson:
            raise NotFound("Lesson not found")
        self.lesson.delete()

    def update(self, lesson_data: dict) -> Lesson:
        subject_uuid = lesson_data.pop("subject_uuid", None)
        if subject_uuid:
            try:
                subject = Subject.objects.get(uuid=subject_uuid)
            except Subject.DoesNotExist:
                raise NotFound("Missing subject")
            self.lesson.subject = subject
        for attr, value in lesson_data.items():
            setattr(self.lesson, attr, value)
        self.lesson.full_clean()
        self.lesson.save()
        return self.lesson
