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

        response = self.client.post("/bells/new", data={"text": "Важные письма"})
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

    def test_create_event_bell_after_POST(self):
        """test: создать событие, после поста запроса"""

        bell = Bell.objects.create()
        response = self.client.post(bell.get_absolute_url_for_events(), data={"text": "Новое письмо от шефа"})
        event = Event.objects.first()
        self.assertEqual(event.bell, bell)
        self.assertEqual(event.text, "Новое письмо от шефа")

    def test_create_event_responds_correctly_to_requests(self):
        """test: адрес для создания событий отвечет корретно"""

        bell = Bell.objects.create()
        response = self.client.post(bell.get_absolute_url_for_events(), data={"text": "Новое письмо от шефа"})
        self.assertEqual(response.status_code, 200)
