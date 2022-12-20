from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.exceptions import ValidationError as RestValidationError

from consailapi.chats.models import Message, Thread
from consailapi.students.models import Student
from consailapi.teachers.models import Teacher


class ThreadService:
    def __init__(self, thread: Thread | None = None):
        self.thread = thread

    @transaction.atomic
    def create(self, thread_data: dict):
        teacher_uuid = thread_data.pop("teacher_uuid")
        student_uuid = thread_data.pop("student_uuid")
        teacher = Teacher.objects.filter(uuid=teacher_uuid).first()
        student = Student.objects.filter(uuid=student_uuid).first()

        thread = Thread(teacher=teacher, student=student)
        try:
            thread.full_clean()
            thread.save()
            self.thread = thread
        except ValidationError as e:
            raise RestValidationError(e.messages)

        return self.thread


class MessageService:
    def __init__(self, message: Message | None = None):
        self.message = message

    @transaction.atomic
    def create(self, thread: Thread, sender: Teacher | Student, message_data: dict):
        message = Message(sender=sender, thread=thread, **message_data)

        try:
            message.full_clean()
            message.save()
            self.message = message
        except ValidationError as e:
            raise RestValidationError(e.messages)
        return self.message
