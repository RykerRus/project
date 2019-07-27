from . import BasePage


class Profile(BasePage):
    
    def __init__(self, browser):
        super().__init__(browser=browser)
        self.elem = {}
    
    def __getattr__(self, item):
        return self.elem[item]
    
    def open(self):
        super().switch_page("/personal/profile/")
        self.browser.is_load_page(wait=10)
        self.browser.is_ajax_complite(wait=10)
        return self
    
    def sumbit(self):
        return self.browser.element("input#btn_save")