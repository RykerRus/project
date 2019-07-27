from . import BasePage

import random

class SluzhbaMontazha(BasePage):
    
    def __init__(self, browser):
        super().__init__(browser=browser)
        self.elem = {}
    
    def __getattr__(self, item):
        return self.elem[item]
    
    def open(self):
        super().switch_page("/garantiya-i-tekhpodderzhka/sluzhba_montazha/")
        self.browser.is_load_page(wait=10)
        self.browser.is_ajax_complite(wait=10)
        return self
    
    def calc(self, name, tel, email, description, service=None):
        self.choice_service(service)
        self.browser.element("input#ORDER_PROP_NAME").value = name
        self.browser.element("input#ORDER_PROP_PHONE").value = tel
        self.browser.element("input#ORDER_PROP_EMAIL").value = email
        self.browser.element("textarea#description").value = description
        
    def choice_service(self, service=None):
        menu = self.browser.element("select.request__form-select")
        menu.hover()
        menu.click()
        options = menu.element("option")
        i = random.randint(0, options.count - 1) if service is None else service
        options[i].hover()
        options.click()

    
    def sumbit(self):
        sumbit = self.browser.element("div.request__button.hidden-xs")
        sumbit.hover()
        sumbit.click()
    
    def check_count_error(self):
        error = self.browser.element("//div[contains(@id, 'result')]", by="xpath")
        return self.browser.wait(error, wait=10).until(lambda e: e.count == 3, message="Количество ошибок не совпадает с заданным")
    
    def check_succes(self):
        return self.browser.element("div.fancybox-skin").visible(wait=10)
