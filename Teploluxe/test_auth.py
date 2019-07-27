from .page.personal import Personal
from .config import browsers, windows_size

import pytest


class TestAuthauthorization:
    _NAME = "Авторизация"
    @pytest.mark.parametrize("capabilities", browsers)
    def test_auth_none(self, browser : "class Browser", capabilities):
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} пустой ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = Personal(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.log_on(login="", password="")
        if not browser.debug:
            page.sumbit()
            assert "Неверный логин или пароль." == page.get_error(), "не совпадает строка ошибки авторизации"
    
    @pytest.mark.parametrize("capabilities", browsers)
    def test_auth_true(self, browser : "class Browser", capabilities):
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = Personal(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.log_on(login="Testal8594212", password="123456")
        if not browser.debug:
            page.sumbit()
            assert page.check_succes(), "ошибка проверки успешности авторизации"
    
    @pytest.mark.parametrize("capabilities", browsers)
    def test_auth_false(self, browser : "class Browser", capabilities):
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} не корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = Personal(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.log_on(login="Test !№;%: 121325", password="Test !№;%: 121325")
        if not browser.debug:
            page.sumbit()
            assert "Неверный логин или пароль." == page.get_error(), "не совпадает строка ошибки авторизации"
