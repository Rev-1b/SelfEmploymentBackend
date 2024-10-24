import uuid

from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['-updated_at']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
