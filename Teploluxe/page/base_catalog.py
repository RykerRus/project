from . import BasePage
from .base_product_page import BaseProductPage
from .order import Order
from selenium.common.exceptions import NoSuchElementException
import random


class BaseCatalog(BasePage):
    
    def __init__(self, browser):
        super().__init__(browser=browser)
        self.elem = {}
        self.base_url = "/bytovye_resheniya"
    
    def __getattr__(self, item):
        return self.elem[item]
    
    def open(self):
        super().switch_page(self.base_url)
        self.browser.is_load_page(wait=10)
        self.browser.is_ajax_complite(wait=10)
    
    def go_to_categories(self):
        block_categories = self.browser.element("div.item-wrap")
        if not block_categories.visible(wait=10):
            raise NoSuchElementException(f"Элементы с ссылками каталога не найдены.{self.browser.url.url}")
        links = block_categories.element("li a")
        url = links[random.randint(0, links.count - 2)].href
        self.browser.open(url)
        self.browser.is_load_page(wait=10)
        self.browser.is_ajax_complite(wait=10)

    def check_catalog(self):
        block_catolog = self.browser.element("div.items-wrap.catalog-list div.item-wrap")
        if not block_catolog.visible(wait=5):
            self.browser.is_load_page(wait=10)
            self.browser.is_ajax_complite(wait=10)
            self.go_to_categories()
            self.check_catalog() # Вославь рекурсию!
    
    def get_btn_to_cart(self):
        products = self.browser.element("div.item-wrap")
        product = products[random.randint(0, products.count - 1)]
        return product.element("a.btn")

    def go_to_order(self, btn_product):
        for _ in range(2):
            btn_product.hover()
            btn_product.click()
        return Order(self.browser)
    
    def filter_block(self):
        return self.browser.element(".main-filter-box")
    
    def btn_filter_block_open(self):
        return self.filter_block().element("a.btn.btn-filter-toggle")
    
    def filter_menu(self, i=0):
        return self.browser.element("div.filter-section.popup-wrap")[i]
    
    def check_box_filter(self, filter_menu, i=0):
        return filter_menu.element("div.frm-select.checkbox")[i]
    
    def go_to_product_page(self, btn_product):
        btn_product.hover()
        btn_product.click()
        return BaseProductPage(self.browser)
    
    def is_choose_param(self, btn_to_cart):
        return not btn_to_cart.is_attr("class=btn-buy")
    
    