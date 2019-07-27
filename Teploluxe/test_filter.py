from .page.base_catalog import BaseCatalog

from .config import browsers, windows_size

import pytest


class TestFilters:
    _NAME = "Фильтры"
    @pytest.mark.parametrize("capabilities", browsers)
    def test_filters_true(self, browser: "class Browser", capabilities, domain):
        
        def check_opened_filter_block():
            flag = capabilities[1] not in "Desktop" and not page.filter_block().is_attr("class=open", wait=2)
            page.btn_filter_block_open().click() if flag else print("Пропуск открытия блока меню")
            
        self.browser = browser
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = BaseCatalog(browser)
        page.base_url += "/elektricheskiy/podobrat_teplyy_pol/"
        page.open()
        browser.driver.set_window_size(1920, 1080)
        check_opened_filter_block()
        filter_menu = page.filter_menu()[1]

        btn_filter_menu_open = filter_menu.element("a.btn-filter")
        btn_filter_menu_open.click() if not btn_filter_menu_open.is_attr("class=active", wait=2) else print("Меню уже открыто")

        first_link = browser.url.url
        check_box = page.check_box_filter(filter_menu)
        check_box.enabled()
        check_box.click()
        browser.wait(browser, wait=5).until(lambda x: x.url.url != first_link, message="Ошибка фильтр не приминился")

        check_opened_filter_block()
        
        first_link = browser.url.url
        check_box[1].click()
        browser.wait(browser, wait=5).until(lambda x: x.url.url != first_link, message="Ошибка фильтр не приминился")
        
        
        