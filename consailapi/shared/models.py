import uuid
from typing import Any

from django.db import models


class UUIDModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, db_index=True, unique=True, editable=False
    )

    class Meta:
        abstract = True

    @property
    def uuid_str(self) -> str:
        return str(self.uuid)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimeStampedModel):
    class Meta:
        abstract = True

    def from_kwargs(self, **kwargs: Any) -> "BaseModel":
        for name, value in kwargs.items():
            setattr(self, name, value)
        return self
