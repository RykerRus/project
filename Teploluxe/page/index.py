from . import BasePage

class Index(BasePage):
    
    def __init__(self, browser):
        super().__init__(browser=browser)
        self.elem = {"tel": browser.element("input[name=form_text_2]")}
    
    def __getattr__(self, item):
        return self.elem[item]
    
    def open(self):
        super().switch_page("/")
        self.browser.is_load_page(wait=10)
        self.browser.is_ajax_complite(wait=10)
        return self
    
    def open_call_back(self):
        btn = self.browser.element("a#callback_button")
        btn.visible(wait=5)
        btn.hover()
        btn.click()

    def call_back(self, name, tel):
        self.tel.visible(wait=10)
        self.tel.value = tel
        self.browser.element("input[name=form_text_1]").value = name
        
    def sumbit(self):
        sumbit = self.browser.element("//div[@name='web_form_1_submit' and contains(text(), 'Заказать звонок')]", by="xpath")
        sumbit.hover()
        sumbit.click()
    
    def is_callback_error(self):
        return self.browser.wait(self.tel, wait=10).until(lambda x: "attention" in x.get_attribute("class"))
    
    def is_callback__succes(self):
        return self.browser.element("div#form_1_thank").visible(wait=10)