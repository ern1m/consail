import uuid

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
