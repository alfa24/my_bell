from django.contrib import admin

# Register your models here.
from bell.models import Bell, Event

admin.site.register(Bell)
admin.site.register(Event)
