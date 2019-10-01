import re
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 20


def wait(fn):
    """декоратор для явного ожидания работы функции"""

    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                # поппытка выполнить функцию
                return fn(*args, **kwargs)

            # если ошибка сравнения или ошибка браузера
            except (AssertionError, WebDriverException) as e:

                # если превышен таймаут, то ошибка
                if time.time() - start_time > MAX_WAIT:
                    raise e

                # если таймаут не вышел, то попробуем выполнить еще разок
                time.sleep(0.5)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    """Функциональный тест"""

    def setUp(self) -> None:
        self.browser = webdriver.Chrome("/usr/bin/chromedriver")

    def tearDown(self) -> None:
        self.browser.quit()

    @wait
    def wait_for_ring(self):
        """ожидать когда зазвенит колокольчик"""

        self.browser.find_element_by_css_selector(".bell .ring")
        # не должно поднять исключение

    @wait
    def wait_for_stop_ring(self):
        """ожидать когда зазвенит колокольчик"""

        self.browser.find_element_by_css_selector(".bell .stop-ring")
        # не должно поднять исключение

    def test_new_bell(self):
        """создать новый колокольчик"""

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
