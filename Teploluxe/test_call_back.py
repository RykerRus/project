from .page.index import Index
from .config import browsers, windows_size

import pytest

class TestCallBack:
    _NAME = "Обратный звонок"
    @pytest.mark.parametrize("capabilities", browsers)
    def test_callback_false(self, browser : "class Browser", capabilities):
        if browsers[1]:
            pytest.skip(f"{self._NAME} только десктоп")
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} не корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = Index(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.open_call_back()
        page.call_back("test 12345 !@#$", "test 12345 !@#$")
        if not browser.debug:
            page.sumbit()
            assert page.is_callback_error()

    @pytest.mark.parametrize("capabilities", browsers)
    def test_callback_none(self, browser : "class Browser", capabilities):
        if browsers[1]:
            pytest.skip(f"{self._NAME} только десктоп")
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} пустой ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = Index(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.open_call_back()
        page.call_back("", "")
        if not browser.debug:
            page.sumbit()
            assert page.is_callback_error()
    
    @pytest.mark.parametrize("capabilities", browsers)
    def test_callback_true(self, browser : "class Browser", capabilities):
        if browsers[1]:
            pytest.skip(f"{self._NAME} только десктоп")
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = Index(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.open_call_back()
        page.call_back("Тестировщик ", "89060834444")
        if not browser.debug:
            page.sumbit()
            assert page.is_callback__succes()