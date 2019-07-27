"""Browser management"""

from __future__ import annotations

import atexit
import re
from contextlib import AbstractContextManager
from typing import Any, Dict, NamedTuple, Optional, Type, Union
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from ..exceptions import NoRunBrowserException
from ..session import Session
from .jquery import JQuery

_BROWSER_MAPPING: Dict[str, Type[webdriver]] = {
    "chrome": webdriver.Chrome,
    "ie": webdriver.Ie,
    "firefox": webdriver.Firefox,
    "opera": webdriver.Opera,
    "remote": webdriver.Remote,
}

_OPTIONS_MAPPING = {
    "chrome": webdriver.ChromeOptions,
    "ie": webdriver.IeOptions,
    "firefox": webdriver.FirefoxOptions,
    "opera": webdriver.ChromeOptions,
}

_MANAGER_MAPPING = {
    "chrome": ChromeDriverManager,
    "ie": IEDriverManager,
    "firefox": GeckoDriverManager,
}

_DEVICE_MAPPING = {"ipad": {"deviceName": "iPad"},
                   "galaxys5": {"deviceName": "Galaxy S5"}}

_FULL_URL_RE = re.compile(r"http(s)?://.+")

class Browser(Session):

    _driver: Optional[webdriver] = None
    __is_browser__ = True
    browser_name: str = None
    options = None
    desired_capabilities = None
    _other_options: dict = None
    base_url: str = None
    _command_executor = "http://testpic.imaginweb.ru:51010/wd/hub/"
    
    def __str__(self):
        import pprint
        return (f"<browser name '{self.browser_name} base url '{self.base_url}' debug '{self.debug}'> \n"
                f"<data {pprint.pformat(self.data)}>\n"
                f"<desired_capabilities {pprint.pformat(self.desired_capabilities)}>")

    def check_running(self):
        if self._driver is None:
            raise NoRunBrowserException("You should open some page before doing anything")

    def __init__(self, browser="chrome", base_url=None, debug=False, handless=False):
        """Init new lazy browser session.
        Setup browser to be used to given local headless browser
        """
        super().__init__(debug)
        self.handless = handless
        self.setup_browser(browser)
        self.base_url = base_url
        self.elem = {}
        self.jquery = JQuery(self)
        atexit.register(self.close_all_windows)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_all_windows()

    def setup_browser(self, browser: str, remote=True, emulation=None,
                      options: Union[webdriver.ChromeOptions, webdriver.FirefoxOptions, webdriver.IeOptions] = None,
                      desired_capabilities: webdriver.DesiredCapabilities = None,
                      **other_options):
        """Configure browser to be used

        :param str browser: Name of browser to be used
        :param bool remote: Is used browser running on remote host.
            In this case you should set `command_executor` argument to desired host value
        :param bool headless: If `options` are not set, control `headless` option
        :param options: Browser options
        :param desired_capabilities: Browser desired capabilities
        :param other_options: Other options which will be passed to WebDriver constructor
        """
        if remote:
            self.browser_name = "remote"
            self.options = options or _OPTIONS_MAPPING[browser]()
        else:
            self.browser_name = browser
            self.options = options
        if options is None:
            self.options = _OPTIONS_MAPPING[browser]()
            self.options.headless = self.handless
        if browser == "chrome" and emulation is not None:
            self.options.add_experimental_option("mobileEmulation", _DEVICE_MAPPING[emulation])
        self.desired_capabilities = desired_capabilities
        self._other_options = other_options

    def __init_browser(self):
        """Start new browser instance"""
        if self._driver is not None:
            return
        browser_cls = _BROWSER_MAPPING[self.browser_name]
        if browser_cls is webdriver.Remote:
            self._driver = webdriver.Remote(command_executor=self._command_executor, desired_capabilities=self.desired_capabilities, options=self.options,
                                  **self._other_options)
            return
        driver_path = _MANAGER_MAPPING[self.browser_name]().install()
        if browser_cls is webdriver.Firefox:
            self._driver = webdriver.Firefox(executable_path=driver_path, options=self.options,
                                   desired_capabilities=self.desired_capabilities, **self._other_options)
        else:
            self._driver = browser_cls(driver_path, options=self.options, **self._other_options)
            
        if self._driver is None: raise NoRunBrowserException()

    def element(self, locator: str, by: str = None, name: str = None, wait=5, scroll=True):
        from .. import Element
        elem_ = Element(self, by=by, locator=locator, wait=wait, scroll=scroll)
        if name is not None:
            self.elem[name] = elem_
        return elem_
    
    def set_driver(self, webdriver: webdriver.Remote):
        """Override lazy driver initialization with already initialized webdriver"""
        if self._driver is not None:
            self._driver.quit()
        self._driver = webdriver
    
    def open(self, url: str = ""):
        from selenium.common.exceptions import InvalidArgumentException
        """Open given URL"""
        self.__init_browser()
        
        if self.base_url and not _FULL_URL_RE.fullmatch(url):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        try:
            self._driver.get(url)
        except InvalidArgumentException as e:
            raise InvalidArgumentException(f"invalid url")
        return self

    def add_cookie(self, cookie_dict: dict):
        """Add cookies to cookie storage"""
        self.check_running()
        self._driver.add_cookie(cookie_dict)
    
    def is_load_page(self, wait=0):
        try:
            return self.wait(self, wait).until(lambda x: x.execute_script("return document.readyState") == "complete", message=f"{self}")
        except TimeoutException:
            return False
    
    def is_ajax_complite(self, wait=0):
        try:
            return self.wait(self, wait).until(lambda x: x.execute_script("return jQuery.active == 0"), message=f"{self}")
        except TimeoutException:
            return False
        

    def close_window(self):
        """Close current browser window"""
        self.check_running()
        self._driver.close()
    
    def close_all_windows(self):
        """Close all browser windows"""
        super().close()
        print(self)
        actual = self._driver
        if actual is not None:
            actual.quit()
            self._driver = None
    
    def get_screenshot_as_png(self):
        """Make new page screenshot"""
        return self._driver.get_screenshot_as_png()
    
    def execute_script(self, script):
        return self.jquery.execute_script(script)
    
    @staticmethod
    def wait(obj, wait=2, frequency=0.5, ignore=None):
            return WebDriverWait(obj, wait, poll_frequency=frequency, ignored_exceptions=ignore)
    
    
    @property
    def url(self) -> URL:
        """Get current page URL"""
        return URL(self._driver.current_url, self.base_url)
    
    @property
    def driver(self):
        """Get browser instance"""
        self.check_running()
        return self._driver

def _url_with_base(base_url: str, url_: str) -> str:
    if base_url is not None:
        if _FULL_URL_RE.fullmatch(url_):
            return url_
        if url_.startswith("/"):
            url_ = url_[1:]
        return f"{base_url}/{url_}"
    return url_

class URL(NamedTuple):
    """Two-part URL"""
    url: str
    base_url: str = None

    def __eq__(self, other: str):
        this = _url_with_base(self.base_url, self.url)
        other = _url_with_base(self.base_url, other)
        return this == other