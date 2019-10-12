import uuid

from django.test import TestCase

from bell.models import Bell, Event


class BellModelTest(TestCase):
    """Тест модели колокольчика"""

    def test_when_saved_an_uuid_created(self):
        """test: При сохранении создается уникальный индефикатор"""

        bell = Bell.objects.create()
        self.assertEqual(bell.link_ref.variant, uuid.RFC_4122)

    def test_get_absolute_url(self):
        """получить абсолютный url"""

        bell = Bell.objects.create()
        self.assertEqual(f'/bells/{bell.link_ref}/', bell.get_absolute_url())

    def test_get_url_for_events(self):
        """получить урл для отправки событий post"""

        bell = Bell.objects.create()
        self.assertEqual(f'/bells/{bell.link_ref}/events/add', bell.get_absolute_url_for_events())

    def test_bell_can_have_title(self):
        """test: колокольчик может иметь заголовок"""

        Bell(title="new bell")
        # не должно поднять исключение
        bell = Bell()
        self.assertEqual(bell.title, "Без названия")


class EventModelTest(TestCase):
    """Тест модели события"""

    def test_event_can_have_bell(self):
        """test: событие привязано к конкретному колокольчику"""

        event = Event(bell=Bell())
        # не должно поднять исключение

    def test_text_default(self):
        """test: текст по умолчанию"""

        event = Event(bell=Bell())
        self.assertEqual(event.text, "")

    def test_read_all_events(self):
        """test: отметить прочтенными все сообщения"""

        bell = Bell.objects.create()
        Event.objects.create(bell=bell)
        Event.objects.create(bell=bell)

        Event.objects.read_all(bell=bell)

        event1 = Event.objects.first()
        event2 = Event.objects.last()
        self.assertTrue(event1.read)
        self.assertTrue(event2.read)

    def test_get_latest_events(self):
        """test: получить последние сообщения"""

        bell = Bell.objects.create()
        Event.objects.create(bell=bell)
        Event.objects.create(bell=bell)

        events = Event.objects.latest(bell=bell)

        event1 = Event.objects.first()
        event2 = Event.objects.last()
        self.assertEqual(events[0], event1)
        self.assertTrue(events[1], event2)
