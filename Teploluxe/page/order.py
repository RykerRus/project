from . import BasePage
from selenium.common.exceptions import NoSuchElementException
import random


class Order(BasePage):
        
    def __init__(self, browser):
        super().__init__(browser=browser)
        self.elem = {"btn_order": browser.element("//a[contains(text(), 'Оформить заказ')]", by="xpath", wait=10)}
    
    def __getattr__(self, item):
        return self.elem[item]

    def order(self, tel, name, email):
        self.browser.element("input#ORDER_PROP_PHONE", wait=10).value = tel
        self.browser.element("input#ORDER_PROP_NAME", wait=2).value = name
        self.browser.element("input#ORDER_PROP_EMAIL", wait=2).value = email
    
    def confirm_order(self):
        btn = self.browser.element("div#bx-soa-orderSave")
        btn.hover()
        btn.click()
    
    def check_succes_order(self):
        succes = self.browser.element("//div[@class='page']/h1[contains(text(), 'Вы оформили заказ')]", by="xpath", wait=10)
        succes.error_msg = "Не найдено подтверждение оформления заказа"
        return succes.visible(wait=10)
    
    def get_error(self):
        e = self.browser.element("div#bx-soa-properties div.alert", wait=10)
        e.error_msg = "Не найдена ошибка"
        return e.visible(wait=10)