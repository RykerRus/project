from .page.sluzhba_montazha import SluzhbaMontazha
from .config import browsers, windows_size

import pytest


class TestSluzhbaMontazha:
    _NAME = "Служба монтажа"
    @pytest.mark.parametrize("capabilities", browsers)
    def test_sluzhbamontazha_none(self, browser: "class Browser", capabilities):
        self.browser = browser
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} пустой ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = SluzhbaMontazha(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.calc(name="", tel="", email="",
                  description="", service=None)  # Если service то выберается рандомно
        if not browser.debug:
            page.sumbit()
            assert page.check_count_error()
    
    @pytest.mark.parametrize("capabilities", browsers)
    def test_sluzhbamontazha_true(self, browser: "class Browser", capabilities):
        self.browser = browser
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = SluzhbaMontazha(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.calc(name="Тестирование", tel="4955438162", email="tester@imaginweb.ru",
                  description="Это автотест от imaginweb.ru", service=None)  # Если service то выберается рандомно
        if not browser.debug:
            page.sumbit()
            assert page.check_succes(), "ошибка проверки успешности авторизации"