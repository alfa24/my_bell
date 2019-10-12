import json
from unittest import skip

from django.test import TestCase
from bell.models import Bell, Event


class HomePageTest(TestCase):
    """тест домашней страницы"""

    def test_uses_home_template(self):
        """тест: используется домашний шаблон"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')


class BellViewTest(TestCase):
    """Тест представления колокольчика"""

    def test_redirect_after_POST(self):
        """test: переадресация после пост-запроса"""

        response = self.client.post("/bells/new", data={"bell_title": "Важные письма"})
        bell = Bell.objects.first()
        self.assertRedirects(response, f"/bells/{bell.link_ref}/")

    def test_uses_bell_template(self):
        """test: представление колокольчика использует шаблон"""

        bell = Bell.objects.create()
        response = self.client.get(f"/bells/{bell.link_ref}/")
        self.assertTemplateUsed(response, "bell.html")

    def test_passes_correct_bell_to_template(self):
        """тест: передает правильный шаблон колокольчика"""

        correct_bell = Bell.objects.create()
        other_bell = Bell.objects.create()

        response = self.client.get(f'/bells/{correct_bell.link_ref}/')
        self.assertEqual(response.context['bell'], correct_bell)

    def test_create_event_responds_correctly_to_requests(self):
        """test: адрес для создания событий отвечет корретно"""

        bell = Bell.objects.create()
        response = self.client.post(bell.get_absolute_url_for_events(), data={"text": "Новое письмо от шефа"})
        self.assertEqual(response.status_code, 200)

    def test_create_new_bell(self):
        """test: Создание колокольчика """

        response = self.client.post("/bells/new", data={"bell_title": "Важные письма"})
        bell = Bell.objects.first()
        self.assertEqual(bell.title, "Важные письма")


class EventViewTest(TestCase):
    """Тест событий колокольчика"""

    def test_create_event_bell_after_POST(self):
        """test: создать событие, после поста запроса"""

        bell = Bell.objects.create()
        response = self.client.post(bell.get_absolute_url_for_events(), data={"text": "Новое письмо от шефа"})
        event = Event.objects.first()
        self.assertEqual(event.bell, bell)
        self.assertEqual(event.text, "Новое письмо от шефа")

    def test_when_creating_an_event_is_unread(self):
        """test: при создании событие является непрочитанным"""

        bell = Bell.objects.create()
        response = self.client.post(bell.get_absolute_url_for_events(), data={"text": "Новое письмо от шефа"})
        event = Event.objects.first()
        self.assertFalse(event.read)

    def test_get_last_unread_event(self):
        """test: Получить последнее непрочитанное событие"""

        bell = Bell.objects.create()
        self.client.post(bell.get_absolute_url_for_events(), data={"text": "Событие 1"})
        self.client.post(bell.get_absolute_url_for_events(), data={"text": "Событие 2"})
        first_event = Event.objects.first()
        seconds_event = Event.objects.last()
        response = self.client.get(f'{bell.get_absolute_url()}events/last/')
        self.assertEqual(response.status_code, 200)
        event = json.loads(response.content)
        self.assertEqual(event["text"], seconds_event.text)
        self.assertEqual(event["read"], seconds_event.read)

    def test_read_all_events(self):
        """test: прочитать все события"""

        bell = Bell.objects.create()
        self.client.post(bell.get_absolute_url_for_events(), data={"text": "Событие 1"})
        self.client.post(bell.get_absolute_url_for_events(), data={"text": "Событие 2"})
        response = self.client.post(f'{bell.get_absolute_url()}events/read')

        self.assertEqual(response.status_code, 302)
        first_event = Event.objects.first()
        seconds_event = Event.objects.last()
        self.assertTrue(first_event.read)
        self.assertTrue(seconds_event.read)

    def test_get_latest_events(self):
        """test: получить последние события"""

        bell = Bell.objects.create()
        self.client.post(bell.get_absolute_url_for_events(), data={"text": "Событие 1"})
        self.client.post(bell.get_absolute_url_for_events(), data={"text": "Событие 2"})
        response = self.client.get(f'{bell.get_absolute_url()}events/latest/')

        self.assertEqual(response.status_code, 200)

        events = json.loads(response.content)
        first_event = Event.objects.first()
        seconds_event = Event.objects.last()
        self.assertEqual(events[0]["text"], first_event.text)
        self.assertEqual(events[1]["text"], seconds_event.text)

    def test_return_empty_list_if_not_events(self):
        """test: вернуть пустой список если нет событий"""

        bell = Bell.objects.create()
        response = self.client.get(f'{bell.get_absolute_url()}events/last/')
        events = json.loads(response.content)
        self.assertEqual({}, events)