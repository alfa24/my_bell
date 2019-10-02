import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

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
