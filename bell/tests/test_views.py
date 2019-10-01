from django.test import TestCase
from bell.models import Bell


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
