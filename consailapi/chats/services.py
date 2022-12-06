from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework.exceptions import ValidationError as RestValidationError

from consailapi.chats.models import Message, Thread
from consailapi.students.models import Student
from consailapi.teachers.models import Teacher


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
