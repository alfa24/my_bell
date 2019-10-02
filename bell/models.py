import uuid

from django.db import models

# Create your models here.
from django.urls import reverse


class Bell(models.Model):
    """модель колокольчика"""

    link_ref = models.UUIDField(default=uuid.uuid4)

    def get_absolute_url(self):
        return reverse('bell_view', args=[self.link_ref])

    def get_absolute_url_for_events(self):
        return reverse('new_event', args=[self.link_ref])


class Event(models.Model):
    """события для колокольчика"""

    bell = models.ForeignKey(Bell, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, default="", blank=True, null=True)
