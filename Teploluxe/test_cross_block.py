from .page.index import BasePage
from .config import browsers, windows_size

import time
import pytest
import random
class TestCrossBlock:
    _NAME = "Кросс блок"
    @pytest.mark.parametrize("capabilities", browsers)
    def test_crossblock(self, browser : "class Browser", capabilities):
        self.browser = browser
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        self.open_product_page_()
        browser.element("div#cross-block").visible(wait=10)
        string = "" if capabilities[1] in "Desktop" else "-mobile" # Изменить селектор ессли мобилка
        nav = browser.element(f"#cross-block{string} div.tabs-nav a", wait=10)
        count_nav = nav.count
        for i in range(0, count_nav):
            nav[i].hover()
            nav.click()
            time.sleep(2)
            self.browser.wait(nav, wait=10).until(lambda n: "active" in n.get_attribute("class"), message="меню кроссблока не переключаются")
            self.check_nav_next(i)
            print("left")
            self.check_nav_prev(i)

    
    def open_product_page_(self):
        self.browser.open("/bytovye_resheniya/elektroustanovochnye-izdeliya2/regulyatory_temperatury/")
        self.browser.driver.set_window_size(1920, 1080)
        self.browser.is_load_page(wait=10)
        self.browser.is_ajax_complite(wait=10)
        links_product = self.browser.element("div.item-wrap .name-block a")
        link = links_product[random.randint(0, links_product.count - 1)]
        link.hover()
        link.click()
  
    def get_transform(self):
        transform = self.browser.element(".item-tab-block.active div.owl-stage").value_of_css_property("transform")
        print(transform.split(" ")[-2][:-1])
        print(transform.split(" "))
        return float(transform.split(" ")[-2][:-1])
    
    def check_nav_next(self, i):
        one = self.get_transform()
        row_left = self.browser.element(".item-tab-block.active .owl-next")
        row_left.hover()
        row_left.click()
        self.browser.wait(self, wait=10).until(lambda two: one > two.get_transform(), message="кнопка вправо не нажимается")
    
    def check_nav_prev(self, i):
        one = self.get_transform()
        row_left = self.browser.element(".item-tab-block.active .owl-prev")
        row_left.hover()
        row_left.click()
        self.browser.wait(self, wait=10).until(lambda two: one < two.get_transform(), message="кнопка влево не нажимается")