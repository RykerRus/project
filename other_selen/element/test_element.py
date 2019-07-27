"""Element wrapper tests"""

import pytest

from ..browser import Browser
from .element import Element


def test_caching(browser, herokuapp_url):
    browser.open(herokuapp_url + "/disappearing_elements")
    element1 = browser.element("div.example p")
    assert element1.get_actual() is element1.get_actual(), "Element is found 2 times"


def test_after_refresh(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/disappearing_elements")
    element1 = browser.element("div.example p")
    e_text1 = element1.get_actual().text
    browser.open("http://google.com")
    browser.open("/disappearing_elements")
    e_text2 = element1.get_actual().text
    assert e_text1 == e_text2


def test_not_existing(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/dynamic_loading/1")
    loading = browser.element("div#loading")
    assert not loading.visible()
    assert not loading.exists()


def test_dynamic_loading(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/dynamic_loading/1")
    start_btn = browser.element("div#start > button")
    finish_txt = browser.element("div#finish")
    loading = browser.element("div#loading")

    assert finish_txt.hidden(wait=5)
    start_btn.click()
    assert start_btn.hidden(wait=5)
    assert loading.visible(wait=5)
    assert loading.hidden(wait=10)
    assert finish_txt.text == "Hello World!"

def test_wait_load_page(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/dynamic_loading/1")
    browser.is_load_page(wait=10)
    browser.is_ajax_complite(wait=10)
    start_btn = browser.element("div#start > button", wait=0)
    finish_txt = browser.element("div#finish", wait=0)
    loading = browser.element("div#loading", wait=0)

    assert finish_txt.hidden(wait=0)
    start_btn.click()
    assert start_btn.hidden(wait=5)
    assert loading.visible(wait=5)
    assert loading.hidden(wait=10)
    assert finish_txt.text == "Hello World!"

def test_search_child(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("dynamic_loading/1")
    root = browser.element("div#content")
    assert root.element("div#start").exists(5)

def test_input_text(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/login")
    form = browser.element("form#login")
    form.element("input#username").value = "tomsmith"
    form.element("input#password").value = "SuperSecretPassword!"
    form.element("button.radius").click()
    assert browser.url == "/secure"
    assert browser.url == f"{herokuapp_url}/secure"


def test_browser_from_nested_element(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/large")
    parent = browser.element("div.exapmple")
    child = parent.element("div#siblings > div", wait=10)
    assert isinstance(child.browser, Browser)


def test_attribute_access(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/forgot_password")
    button = browser.element("#form_submit")

    assert button.id == button.get_attribute("id")
    assert button.type == button.get_attribute("type")


def test_checkboxes(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/checkboxes")
    form = browser.element("form#checkboxes")

    children = form.element("input")

    ch1 = children[0]
    assert not ch1.is_selected()
    ch1.click()
    assert ch1.is_selected()

    ch2 = children[1]
    assert ch2.is_selected()
    ch2.click()
    assert not ch2.is_selected()


def test_element_hover(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/hovers")
    figures = browser.element("div.figure")

    def _re_usr_covert(_link: str):
        part1, part2 = _link.split("/")[-2:]
        return f"{part1[:-1]}{part2}"

    for single in range(figures.count):  # type: Element
        image = figures[single].element("img")
        caption = figures[single].element("div.figcaption")

        image.hover()
        caption.visible(wait=5)
        link = caption.element("a")
        assert caption.element("h5").text == f"name: {_re_usr_covert(link.href)}"
        assert link.text == "View profile"


def test_element_parent(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/login")
    username = browser.element("#username")
    div = username.parent_elem
    assert div.tag_name == "div"


def test_clear(browser ,herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/login")
    username = browser.element("#username")
    username.value = "let me speak"
    username.value = ""
    assert username.text == ""


def test_value(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/dropdown")
    dropdown = browser.element("#dropdown")
    options = dropdown.element("option")
    assert options[0].value == ""
    assert options[1].value == "1"
    assert options[2].value == "2"


@pytest.fixture
def _prepare_menu(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/jqueryui/menu")
    disabled = browser.element("#ui-id-1")
    enabled = browser.element("#ui-id-2")
    return enabled, disabled


def test_enabled(_prepare_menu):
    enabled, disabled = _prepare_menu
    assert enabled.enabled()
    assert not disabled.enabled()


def test_disabled(_prepare_menu):
    enabled, disabled = _prepare_menu
    assert disabled.disabled()
    assert not enabled.disabled()

"""
def test_ancestors(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/login")
    form = browser.element("#login")
    divs = form.ancestors()
    assert divs.count == 5


def test_ancestors_filter(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/login")
    form = browser.element("#login")
    divs = form.ancestors(lambda e: e.tag_name == "div")
    assert divs.count == 3


def test_neighbours(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/login")
    inputs = browser.element("#username").neighbours()
    assert inputs.count == 2


def test_neighbours_filter(browser, herokuapp_url):
    browser.base_url = herokuapp_url
    browser.open("/login")
    username = browser.element("#username")
    not_input = username.neighbours(lambda e: e.tag_name == "label")
    assert not_input.count == 1"""


