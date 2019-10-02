from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest

MAX_WAIT = 10


class LayoutAndStylingTest(FunctionalTest):
    """тест макета и стилевого оформления"""

    def test_layout_and_styling(self):
        """тест макета и стиля"""

        # Иван открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Он замечает что поле ввода аккуратно центрировано
        inputbox = self.get_bell_title_inputbox()
        self.assertAlmostEqual(
            inputbox.location['x'] + (inputbox.size['width'] + 60) / 2,
            512,
            delta=10
        )

        # он создает новый колокольчик и видит, что там тоже поле центрировано
        self.add_new_bell('Сообщение в чате')
        bell_title = self.browser.find_element_by_css_selector(".bell-title")
        self.assertAlmostEqual(
            bell_title.location['x'] + bell_title.size['width'] / 2,
            512,
            delta=10
        )
