import os
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
    """Базовый функциональный тест"""

    def setUp(self) -> None:
        self.browser = webdriver.Chrome("/usr/bin/chromedriver")
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = f'http://{self.staging_server}'

    def tearDown(self) -> None:
        self.browser.quit()

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_for_ring(self):
        """ожидать когда зазвенит колокольчик"""

        self.browser.find_element_by_css_selector(".bell-status.ring")
        # не должно поднять исключение

        # кнопка выключить отображается
        read_button = self.browser.find_element_by_css_selector(".bell-status__read")
        self.assertTrue(read_button.is_displayed())

    @wait
    def wait_for_stop_ring(self):
        """ожидать когда зазвенит колокольчик"""

        self.browser.find_element_by_css_selector(".bell-status.not-ring")
        # не должно поднять исключение

        # на экране сообщение, о том что колокольчик ждет уведомлений
        text = self.browser.find_element_by_css_selector('.bell-status__text').text
        self.assertIn('Ждем события....', text)

        # кнопка выключить скрыта
        read_button = self.browser.find_element_by_css_selector(".bell-status__read")
        self.assertFalse(read_button.is_displayed())

    def send_event_to_bell(self, url, text):
        self.client.post(url, data={'text': text})

    def get_bell_title_inputbox(self):
        """Получить поле ввода имени колокольчика"""

        return self.browser.find_element_by_id("id_bell_title")

    def add_new_bell(self, title):
        """Создать новый колокольчик"""

        self.browser.get(self.live_server_url)
        new_bell_inputbox = self.get_bell_title_inputbox()
        self.assertEqual(new_bell_inputbox.get_attribute("placeholder"), "Введите имя для колокольчика")
        new_bell_inputbox.send_keys(title)
        new_bell_inputbox.send_keys(Keys.ENTER)
