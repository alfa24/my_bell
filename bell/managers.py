from django.db.models import Manager


class EventManager(Manager):
    """менеджер событий"""

    def read_all(self, bell):
        """отметить прочтенными все сообщения"""
        self.filter(bell=bell).update(read=True)

    def latest(self, bell):
        """получить последние сообщения"""
        return self.filter(bell=bell)[:10]
