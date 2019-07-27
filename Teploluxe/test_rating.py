from .page.base_catalog import BaseCatalog

from .config import browsers, windows_size

import pytest


class TestRating:
    _NAME = "Рейтинг товаров"
    
    @pytest.mark.parametrize("capabilities", browsers)
    def test_rating_true(self, browser: "class Browser", capabilities, domain):
        
        self.browser = browser
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = BaseCatalog(browser)
        page.base_url += "/truby-dlya-teplykh-polov-i-vodosnabzheniya/fitingi/"
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.check_catalog()
        btn = page.get_btn_to_cart()
        
        product_page = page.go_to_product_page(btn)
        product_page.open_rating_menu()
        product_page.open_comment_form()
        product_page.add_comment(name="Авто-тест Imaginweb", email="tester@imaginweb.ru", comment='Авто-тест Imaginweb')

        if not browser.debug:
            product_page.sumbit_comment_form()
            assert product_page.check_succes_comment(), domain

