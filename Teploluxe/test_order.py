from .page.base_catalog import BaseCatalog

from .config import browsers, windows_size

import pytest, time


class TestOrder:
    _NAME = "Оформление"
    @pytest.mark.parametrize("capabilities", browsers)
    def test_order_true(self, browser: "class Browser", capabilities, domain):
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = BaseCatalog(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.go_to_categories()
        page.check_catalog()
        btn_add_to_cart = page.get_btn_to_cart()
        page_order = None
        if page.is_choose_param(btn_add_to_cart):
            page_product = page.go_to_product_page(btn_add_to_cart)
            page_product.open_menu_choose()
            page_product.choose_option()
            assert page_product.add_to_cart(), "Не найдена кнопка оформления заказа"
            time.sleep(3)
            page_order = page_product.go_to_order()
        else:
            page_order = page.go_to_order(btn_add_to_cart)
        if page_order is None:
            assert False, "Ошибка добавления товара в корзину"
        page_order.order(tel="4955438162", name="Авто-тест Imaginweb", email="tester@imaginweb.ru")
        if not browser.debug:
            page_order.confirm_order()
            assert page_order.check_succes_order(), domain

    
    @pytest.mark.parametrize("capabilities", browsers)
    def test_order_none(self, browser: "class Browser", capabilities, domain):
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = BaseCatalog(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.go_to_categories()
        page.check_catalog()
        btn_add_to_cart = page.get_btn_to_cart()
        page_order = None
        if page.is_choose_param(btn_add_to_cart):
            page_product = page.go_to_product_page(btn_add_to_cart)
            page_product.open_menu_choose()
            page_product.choose_option()
            assert page_product.add_to_cart(), "Не найдена кнопка оформления заказа"
            time.sleep(3)
            page_order = page_product.go_to_order()
        else:
            page_order = page.go_to_order(btn_add_to_cart)
        if page_order is None:
            assert False, "Ошибка добавления товара в корзину"
        page_order.order(tel="", name="", email="")
        if not browser.debug:
            page_order.confirm_order()
            assert page_order.check_succes_order(), domain
