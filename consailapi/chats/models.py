from django.db import models
from django.utils.translation import gettext_lazy as _

from consailapi.shared.models import BaseModel
from consailapi.students.models import Student
from consailapi.teachers.models import Teacher
from consailapi.users.models import User


class Thread(BaseModel):
    teacher = models.ForeignKey(
        Teacher,
        verbose_name=_("teacher"),
        related_name="threads",
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        Student,
        verbose_name=_("student"),
        related_name="threads",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("thread")
        verbose_name_plural = _("threads")
        unique_together = (("teacher", "student"),)

    def __str__(self):
        return self.uuid_str


class Message(BaseModel):
    sender = models.ForeignKey(
        User,
        verbose_name=_("sender"),
        related_name="messages",
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    thread = models.ForeignKey(
        Thread,
        verbose_name=_("thread"),
        related_name="messages",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")
        ordering = ("-created_at",)
