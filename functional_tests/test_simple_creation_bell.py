import re

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
        self.assertIn('Мой колокольчик', header_text)

        # Он видит поле для ввода названия колокольчика
        new_bell_iputbox = self.browser.find_element_by_id("id_new_bell_title")
        self.assertEqual(new_bell_iputbox.get_attribute("placeholder"), "Введите имя для колокольчика")
        new_bell_iputbox.send_keys("Важные письма")
        new_bell_iputbox.send_keys(Keys.ENTER)

        # И попадает на страницу нового колокольчика
        self.assertEqual(self.browser.title, "Колокольчик: Важные письма")
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Важные письма', header_text)

        # Он видит сообщение, что колокольчик ждет события
        text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Ждем события....', text)

        # Так же он видит адрес и информацию, для отправки уведомлений на этот колокольчик методом пост-запросов
        address_for_post = self.browser.find_element_by_id('id_address_for_post').text
        url_search = re.search(r'http://.+/bells/.+$', address_for_post)
        if not url_search:
            self.fail(f'Не найден адрес для пост-запроса.')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # он отправляет пост-запрос из другого приложения на этот адрес
        self.client.post(url, data={'text': 'Новое письмо от Владимира!'})

        # колокольчик начинает звенеть
        self.wait_for_ring()

        # и на экран выходит сообщение
        message = self.browser.find_element_by_id('id_message').text
        self.assertEqual(message, 'Новое письмо от Владимира!')

        # Иван нажимает кнопку "Остановить"
        stop_ring = self.browser.find_element_by_link_text("Остановить")
        stop_ring.click()

        # Звонок останавливается
        self.wait_for_stop_ring()

        # и на экране опять сообщение, о том что колокольчик ждет уведомлений
        text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Ждем события....', text)
