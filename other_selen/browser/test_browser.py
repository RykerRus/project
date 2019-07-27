from .browser import Browser, URL
from ..exceptions import NoRunBrowserException
import pytest

from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions, Remote
from webdriver_manager.firefox import GeckoDriverManager

def test_open():
    browser = Browser(base_url="http://ya.ru/").open()
    browser.element("html").get_actual()

def test_close_all():
    """Check that all browser windows are closed"""
    browser = Browser(base_url="http://ya.ru")
    browser.open()
    browser.close_all_windows()
    with pytest.raises(NoRunBrowserException):
        browser.element("html").get_actual()

def test_close_all_not_started():
    brw = Browser(base_url="http://ya.ru")
    brw.close_all_windows()
    

def test_closed_with_context():
    with Browser(base_url="http://ya.ru") as brw:
        brw.close_all_windows()

def test_close_all_reopen():
    with Browser(base_url="http://ya.ru") as brw:
        brw.close_all_windows()
        brw.open()


def test_no_open_page():
    with Browser(base_url="http://ya.ru") as browser:
        el = browser.element("html")
        with pytest.raises(NoRunBrowserException):
            el.get_actual()

def test_chrome():
    with Browser(browser="chrome", base_url="http://ya.ru") as browser:
        browser.open("/disappearing_elements")
        browser.element("html").get_actual()


def test_firefox():
    with Browser(browser="firefox", base_url="http://ya.ru") as browser:
        browser.open("/disappearing_elements")
        browser.element("html").get_actual()
        browser.close_all_windows()

    
def test_url_check(base_url="http://ya.ru"):
    """No exceptions is enough here"""
    with Browser(browser="firefox", base_url=base_url) as browser:
        url = "/disappearing_elements"
        browser.open(url)
        assert browser.url == f"{base_url}{url}"

def test_set_driver(base_url="http://ya.ru"):
    with Browser(browser="firefox") as browser:
        options = FirefoxOptions()
        options.headless = True
        browser.set_driver(Firefox(options=options, executable_path=GeckoDriverManager().install()))
        assert isinstance(browser._driver, Firefox)  # not lazy!
        browser.open(base_url)
        
def test_replace_driver(base_url="http://ya.ru"):
    with Browser(browser="firefox") as browser:
        browser.open(base_url)
        options = FirefoxOptions()
        options.headless = True
        browser.set_driver(Firefox(options=options, executable_path=GeckoDriverManager().install()))
        assert isinstance(browser._driver, Firefox)  # not lazy!
        browser.open(base_url)

def test_no_base_url():
    actual = "dfsbhjhjdgflslidgfsn"
    url = URL(actual, None)
    assert url.base_url is None
    assert url.url == actual
    assert url == actual