from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class FunctionalTest(StaticLiveServerTestCase):
    """Функциональный тест"""

    def setUp(self) -> None:
        self.browser = webdriver.Chrome("/usr/bin/chromedriver")

    def tearDown(self) -> None:
        self.browser.quit()

    def test_new_bell(self):
        """создать новый колокольчик"""

        # Иван заходит на сайт
        self.browser.get("http://127.0.0.1:8000")

        # Видит заголовок сайта "Мой колокольчик"
        self.assertEqual(self.browser.title, "Мой колокольчик")
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Мой колокольчик', header_text)

        # Он видит поле для ввода названия колокольчика
        new_bell_iputbox = self.browser.find_element_by_id("id_new_bell")
        self.assertEqual(new_bell_iputbox.get_attribute("placeholder"), "Введите имя для колокольчика")
        new_bell_iputbox.send_keys("Важные письма")
        new_bell_iputbox.send_keys(Keys.ENTER)

        # И попадает на страницу нового колокольчика
        self.fail("дописать")

        # Он видит сообщение, что колокольчик ждет события

        # Так же он видит адрес и информацию, для отправки уведомлений на этот колокольчик методом пост-запросов

        # он отправляет пост-запрос из другого приложения на этот адрес

        # колокольчик начинает звенеть и на экран выходит сообщение

        # Иван нажимает кнопку "Остановить звон"

        # Звонок останавливается и на экране опять сообщение, о том что колокольчик ждет уведомлений
