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
