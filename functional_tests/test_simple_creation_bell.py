import re
from unittest import skip

from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    """Функциональный тест для нового посетителя"""

    def test_can_create_new_bell(self):
        """тест: создать новый колокольчик"""

        # Иван заходит на сайт
        self.browser.get(self.live_server_url)

        # Видит заголовок сайта "Мой колокольчик"
        self.assertEqual(self.browser.title, "Мой колокольчик")
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Создай свой колокольчик!', header_text)

        # Он видит поле для ввода названия колокольчика
        self.add_new_bell("Важные письма")

        # И попадает на страницу нового колокольчика
        self.assertEqual(self.browser.title, "Колокольчик: Важные письма")
        header_text = self.browser.find_element_by_css_selector('.bell-title').text
        self.assertEqual('Важные письма', header_text)

        # Он видит сообщение, что колокольчик ждет события
        self.wait_for_stop_ring()

    def test_ring_bell_after_post_request(self):
        """тест: колокольчик звенит после пост-запроса"""

        # Ивано создает новый колокольчик
        self.add_new_bell("Важные письма")

        # Теперь он видит адрес и информацию, для отправки уведомлений на этот колокольчик методом пост-запросов
        address_for_post = self.browser.find_element_by_css_selector('.bell-info').text
        url_search = re.search(r'http://.+/bells/.+/events/add', address_for_post)
        if not url_search:
            self.fail(f'Не найден адрес для пост-запроса.')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Так как нет событий, то колокольчик молчит
        self.wait_for_stop_ring()

        # он отправляет пост-запрос из другого приложения на этот адрес
        self.client.post(url, data={'text': 'Новое письмо от Владимира!'})

        # колокольчик начинает звенеть
        self.wait_for_ring()

        # и на экран выходит сообщение
        message = self.browser.find_element_by_css_selector('.bell-status__text').text
        self.assertEqual(message, 'Новое письмо от Владимира!')

        # Иван нажимает кнопку "Выключить"
        stop_ring = self.browser.find_element_by_css_selector(".bell-status__read")
        stop_ring.click()

        # Звонок останавливается
        self.wait_for_stop_ring()


