from . import BasePage


class Parthnership(BasePage):
    
    def __init__(self, browser):
        super().__init__(browser=browser)
        self.elem = {}
    
    def __getattr__(self, item):
        return self.elem[item]
    
    def open(self):
        super().switch_page("/about/partnership/")
        self.browser.is_load_page(wait=10)
        self.browser.is_ajax_complite(wait=10)
        return self
    
    def partnership(self, name, tel, email):
        self.browser.element("input[name=form_text_3]").value = name
        self.browser.element("input[name=form_text_8]").value = tel
        self.browser.element("input[name=form_email_9]").value = email
    
    def sumbit(self):
        sumbit = self.browser.element("input[value='Отправить заявку']")
        sumbit.hover()
        sumbit.click()
    
    def get_error(self):
        return self.browser.element("font.errortext")[1].text
    
    def check_succes(self):
        super().switch_page("/personal/profile/")
        return self.browser.element("//div[@class='news-box']//div[contains(text(), 'заявка  принята')]", by="xpath").visible(wait=10)
