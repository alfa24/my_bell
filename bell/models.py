import uuid

from django.db import models

# Create your models here.
from django.urls import reverse


class Bell(models.Model):
    """модель колокольчика"""

    link_ref = models.UUIDField(default=uuid.uuid4)

    def get_absolute_url(self):
        return reverse('bell_view', args=[self.link_ref])
