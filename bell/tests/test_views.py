from django.test import TestCase


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
        self.assertRedirects(response, "/bells/1/")

    def test_uses_bell_template(self):
        """test: представление колокольчика использует шаблон"""

        response = self.client.get("/bells/1/")
        self.assertTemplateUsed(response, "bell.html")
