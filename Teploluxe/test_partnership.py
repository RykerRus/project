from .page.pathnership import Parthnership
from .config import browsers

import pytest


class TestOrder:
    _NAME = "Стать партнером"
    
    @pytest.mark.parametrize("capabilities", browsers)
    def test_partnership_true(self, browser: "class Browser", capabilities, domain):
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = Parthnership(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.partnership(name="Авто-тест Imaginweb", tel="4955438162", email="tester@imaginweb.ru")
        if not browser.debug:
            page.sumbit()
            assert page.check_succes_order(), domain
    
    @pytest.mark.parametrize("capabilities", browsers)
    def test_partnership_none(self, browser: "class Browser", capabilities, domain):
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = Parthnership(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.partnership(name="Авто-тест Imaginweb", tel="4955438162", email="tester@imaginweb.ru")
        if not browser.debug:
            page.sumbit()
            alert_error_text = '''Не заполнены следующие обязательные поля:\n  » "ФИО"\n  » "Телефон"\n  » "E-mail"'''
            assert alert_error_text == page.get_error(), "Тексты уведомления о незаполненных полях не совпадают"
