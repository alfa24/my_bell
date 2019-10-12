import json

from django.db.models import Manager


class EventManager(Manager):
    """менеджер событий"""

    def read_all(self, bell):
        """отметить прочтенными все сообщения"""
        self.filter(bell=bell).update(read=True)

    def latest(self, bell):
        """получить последние сообщения"""
        return self.filter(bell=bell).order_by("-created_at")[:10]

    def latest_data(self, bell):
        """получить последние сообщения в формате json"""

        result = []
        qs = self.latest(bell)
        for e in qs:
            result.append(
                {
                    "text": e.text,
                    "date": e.created_at.strftime("%d.%m.%y %H:%M:%S")
                }
            )

        return result
