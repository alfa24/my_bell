import datetime
import json
import uuid
from unittest import mock

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

    def test_bell_string_representation(self):
        """test: строковое представление колокольчика"""

        bell = Bell.objects.create(title="new bell")
        self.assertEqual(str(bell), "new bell")


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

    @mock.patch('django.utils.timezone.now')
    def test_event_has_creation_date(self, today_mock):
        """test: событие содержит дату создания"""

        created_at = datetime.datetime.now()
        today_mock.return_value = created_at
        bell = Bell.objects.create()
        event = Event.objects.create(bell=bell)
        self.assertEqual(event.created_at, created_at)

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
        self.assertEqual(events[0], event2)
        self.assertTrue(events[1], event1)

    def test_latest_events_sorted_desc(self):
        """test: Последние события отсортированы в порядке убывания"""

        bell = Bell.objects.create()
        e1 = Event.objects.create(bell=bell)
        e2 = Event.objects.create(bell=bell)

        events = Event.objects.latest(bell=bell)
        self.assertEqual(events[0], e2)
        self.assertEqual(events[0], e2)


    def test_get_latest_json_events(self):
        """test: получить последние сообщения в формате json"""

        bell = Bell.objects.create()
        Event.objects.create(bell=bell)
        Event.objects.create(bell=bell)

        events = Event.objects.latest_data(bell=bell)

        event1 = Event.objects.first()
        event2 = Event.objects.last()

        self.assertEqual(events[0]["text"], event1.text)
        self.assertEqual(events[0]["date"], event1.created_at.strftime("%d.%m.%y %H:%M:%S"))
        self.assertEqual(events[1]["text"], event2.text)
        self.assertEqual(events[1]["date"], event2.created_at.strftime("%d.%m.%y %H:%M:%S"))
