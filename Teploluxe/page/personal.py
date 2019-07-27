from . import BasePage

class Personal(BasePage):
    
    def __init__(self, browser):
        super().__init__(browser=browser)
        self.elem = {}
    
    def __getattr__(self, item):
        return self.elem[item]

    def open(self):
        super().switch_page("/personal/")
        self.browser.is_load_page(wait=10)
        self.browser.is_ajax_complite(wait=10)
        return self

    def log_on(self, login, password):
        self.browser.element("input[name=USER_LOGIN]")[1].value = login
        self.browser.element("input[name=USER_PASSWORD]")[1].value = password
    
    def sumbit(self):
        sumbit = self.browser.element("input[name=Login]")[1]
        sumbit.hover()
        sumbit.click()
    
    def get_error(self):
        return self.browser.element("font.errortext")[1].text
    
    def check_succes(self):
        super().switch_page("/personal/profile/")
        return self.browser.element("div.frm-row input#NAME").visible(wait=10)
    
    def open_reg_form(self):
        btn = self.browser.element("//a[contains(text(), 'Регистрация')]", by="xpath")[2]
        btn.hover()
        btn.click()
    
    def registration(self, login, password, password_confirm):
        self.browser.element("input[name='REGISTER[LOGIN]']").value = login
        self.browser.element("input[name='REGISTER[PASSWORD]']").value = password
        self.browser.element("input[name='REGISTER[CONFIRM_PASSWORD]']").value = password_confirm
    
    def registration_sumbit(self):
        return self.browser.element("input[name='register_submit_button']")
    
    def get_registration_error(self):
        return self.browser.element("font.errortext").text
    
    