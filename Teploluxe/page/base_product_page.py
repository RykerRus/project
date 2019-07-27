from . import BasePage
from .order import Order
from selenium.common.exceptions import NoSuchElementException
import random, time


class BaseProductPage(BasePage):
    
    def __init__(self, browser):
        super().__init__(browser=browser)
        self.elem = {"btn_order": browser.element("//a[contains(text(), 'Оформить заказ')]", by="xpath", wait=10)}
    
    def __getattr__(self, item):
        return self.elem[item]

    def open_menu_choose(self):
        menu_choose = self.browser.element(".tp_value.fancybox")
        menu_choose.hover()
        menu_choose.click()
    
    def choose_option(self, option_number=None):
        options = self.browser.element("table#tp_filtr tbody tr.tp_filtr")
        i = random.randint(1, options.count - 1) if option_number is None else option_number
        option = options[i]
        option.hover()
        self.browser.execute_script(("arguments[0].click();", option.get_actual()))
        
    def add_to_cart(self):
        btn = self.browser.element("//a[contains(text(), 'В корзину')]", by="xpath", wait=10)
        btn.hover()
        btn.click()
        return self.btn_order.visible(wait=10)
    
    def go_to_order(self):
        pop_up = self.browser.element("//div[@class='fancybox-skin']//a[@title='Close']", by="xpath", wait=5)
        if pop_up.visible():
            pop_up.hover()
            pop_up.click()
        time.sleep(2)
        self.btn_order.hover()
        self.btn_order.click()
        return Order(self.browser)
    
    def open_rating_menu(self):
        btn = self.browser.element("a#tab_comment_add_rating")
        if not btn.is_attr("class=active"):
            btn.hover()
            btn.click()
        else:
            print("Меню уже открыто")
    
    def open_comment_form(self):
        self.browser.element("div.blog-add-comment a").click()
    
    def add_comment(self, name, email, comment):
        comment_block = self.browser.element("div.blog-comment-fields")
        comment_block.error_msg = "Ошибка блок комментария отстутствует на странице"
        assert comment_block.visible(wait=2), "Ошибка блок комментария скрыт"
        
        comment_block.element("input#user_name").value = name
        comment_block.element("input#user_email").value = email
        self.browser.execute_script(f"$('iframe#LHE_iframe_LHEBlogCom').contents().find('body').append('{comment}')")
        comment_block.element("input[name=captcha_word]").value = self._bake_captcha(comment_block)


    def _bake_captcha(self, comment_block):
        import requests
        from requests.exceptions import InvalidURL
        from captcha_solver import CaptchaSolver
        
        url_image = comment_block.element("img#captcha").src
        try:
            get_img = requests.get(url_image, stream=True)
        except InvalidURL:
            capthca_url_without_auth = url_image.replace('t:123456%@', '') + '.jpeg'
            get_img = requests.get(capthca_url_without_auth, stream=True, auth=('t', '123456%'))
    
        with open('captcha_rating.jpeg', 'wb') as fd:
            for chunk in get_img.iter_content(chunk_size=128):
                fd.write(chunk)
        solver = CaptchaSolver('antigate', api_key='3d756e5391dd1e1423739217e6579c1a')
        raw_data = open('captcha_rating.jpeg', 'rb').read()
    
        return solver.solve_captcha(raw_data)
        
    def sumbit_comment_form(self):
        btn = self.browser.element("div.blog-comment-buttons input")
        btn.hover()
        btn.click()
    
    def check_succes_comment(self):
        self.browser("//div[@class='blog-textinfo-text' and"
                     " contains(text(), 'Ваш комментарий добавлен')]", by="xpath", wait=5).visible(wait=10)
    