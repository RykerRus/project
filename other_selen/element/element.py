"""WebElement wrappers"""
from __future__ import annotations

import time
from typing import Callable, Sequence, Union

import wrapt
from selenium.common.exceptions import (
    WebDriverException, TimeoutException, InvalidArgumentException, MoveTargetOutOfBoundsException,
    ElementNotInteractableException)
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from ..browser import Browser

class Element:
    
    def __init__(self, browser, locator, parent=None, by=None, wait=5, scroll=True):
        self.browser = browser
        self.parent = parent
        self.locator = locator
        self.by = by
        self.__cached__ = None
        self.index = 0
        self.wait = wait
        self.scroll = scroll
        self._error_msg = self.__str__()

    def __str__(self):
        return f"<selector {self.locator}, {self.by},  index '{self.index}'  wait '{self.wait}'>"
    
    def __getitem__(self, given):
        if isinstance(given, slice):
            self.get_actual()
            return self.__cached__[given]
        else:
            # Do your handling for a plain index
            self.index = given
            self.__cached__ = None
        return self
    
    def find_by(self, wait=None):
        wait = self.wait if wait is None else wait
        if self.by is None:
            self.by = By.CSS_SELECTOR
        elif self.by == "xpath":
            self.by = By.XPATH
         
        parent = self.browser.driver if self.parent is None else self.parent.get_actual()
        try:
            self.__cached__ = self.browser.wait(parent, wait=wait).until(lambda x: x.find_elements(self.by, self.locator), message=f"{self}")
        except InvalidArgumentException:
            raise InvalidArgumentException(f"invalid locator {self}")

    def _element_is_dead(self):
        try:
            _ = self.__cached__[self.index].location
            return False
        except WebDriverException:
            return True
    
    def getBoundingClientRect(self):
        self.error_msg = "Не найден элемент"
        return self.browser.execute_script(("return arguments[0].getBoundingClientRect();", self.get_actual()))

    def _scroll(self):
            if self.scroll:
                view_height = self.browser.execute_script("return document.body.clientWidth")
                loc = self.getBoundingClientRect()
                yoffset = loc["top"] + (loc["height"] / 2)
                y = yoffset - view_height / 2
                if yoffset < 200 or yoffset > view_height - 200:
                    self.browser.execute_script(f"window.scrollBy(0, {y})")
            time.sleep(0.5)
    
    def get_actual(self, wait=None) -> WebElement:
        """Get element, check if it's cached or already dead"""
        self.browser.check_running()
        if (self.__cached__ is None) or self._element_is_dead():
            self.find_by(wait=wait)
        return self.__cached__[self.index]

    def click(self):
        """Click web element"""
        self._scroll()
        try:
            self.get_actual().click()
        except ElementNotInteractableException as e:
            raise ElementNotInteractableException(f"{e.msg}\n{self}")

    def double_click(self):
        """Make double click on the element"""
        self._scroll()
        actions = ActionChains(self.browser.get_actual())
        actions.double_click(self.get_actual())

    @property
    def location(self):
        """Get current element location"""
        return self.get_actual().location

    def hover(self):
        """Hover over element"""
        self._scroll()
        actions = ActionChains(self.browser.driver)
        try:
            actions.move_to_element(self.get_actual()).perform()
        except MoveTargetOutOfBoundsException as e:
            raise MoveTargetOutOfBoundsException(f"{e.msg}\n{self}")

    def right_click(self):
        """Open context menu"""
        self._scroll()
        actions = ActionChains(self.browser.driver)
        actions.context_click(self.get_actual()).perform()
    
    def get_attribute(self, name: str) -> str:
        """Get WebElement attribute value"""
        return str(self.get_actual().get_attribute(name))
    
    def is_attr(self, string: str, wait=0) -> bool:
        """
        string use:
            name_atr=value_atr
        example
            class=active"""
        name_attr, value_attr = string.split("=")
        try:
            return self.browser.wait(self, wait=wait).until(lambda x: value_attr in x.get_attribute(name_attr))
        except TimeoutException:
            return False

    @property
    def count(self):
        return len(self[:])

    @property
    def text(self) -> str:
        """Get element text"""
        return self.get_actual().text

    @property
    def value(self):
        """Get element @value attribute"""
        return self.get_actual().get_attribute("value")

    def clear(self):
        """Clear input field"""
        self.get_actual().clear()

    @value.setter
    def value(self, value: str):
        """Set element text (if possible)"""
        self._scroll()
        self.clear()
        self.get_actual().send_keys(value)
        
    def visible(self, wait=0):
        """Check if element is visible"""
        if not self.exists(wait):
            return False
        try:
            return self.browser.wait(self, wait).until(lambda e: e.get_actual().is_displayed(), message=self._error_msg)
        except TimeoutException:
            return False

    def hidden(self, wait=0):
        """Check if element is hidden"""
        if not self.exists(wait):
            return True
        try:
            return self.browser.wait(self, wait).until(lambda e: not e.get_actual().is_displayed(), message=self.time_error_msg)
        except TimeoutException:
            return False

    def is_selected(self, wait=0):
        """Return element selected state"""
        try:
            return self.browser.wait(self, wait).until(lambda e: e.get_actual().is_selected(), message=self._error_msg)
        except TimeoutException:
            return False

    def enabled(self, wait=0):
        """Return element enabled state"""

        def _enabled(_el: WebElement):
            enab = _el.is_enabled()
            disab = _el.get_attribute("disabled") or _el.get_attribute("aria-disabled")
            return enab and not disab

        try:
            return self.browser.wait(self, wait).until(lambda e: _enabled(e.get_actual()), message=self._error_msg)
        except TimeoutException:
            return False

    def disabled(self, wait=0):
        """Return element disabled state"""
        try:
            return not self.browser.wait(self, wait).until_not(lambda e: e.enabled(), message=self._error_msg)
        except TimeoutException:
            return False

    @property
    def tag_name(self):
        """Get element tag name"""
        return self.get_actual().tag_name

    # TODO: re-enable if become useful
    # @_should_exit
    # def get_property(self, name):
    #     """Gets the given property of the element"""
    #     self.get_actual().get_property(name)

    @property
    def size(self):
        """Element size"""
        return self.get_actual().size

    def value_of_css_property(self, name):
        """Returns value css property"""
        return self.get_actual().value_of_css_property(name)

    @property
    def parent_elem(self):
        """Return parent element of given one"""
        return self.element(by="xpath", locator="./..")
    
    def element(self, locator: str, by: str = None, wait=5):
        return Element(self.browser, parent=self, by=by, locator=locator, wait=wait)
    
    def exists(self, wait=0):
        """Check if element exists in dom"""
        try:
            self.get_actual(wait=wait)
            return True
        except TimeoutException:
            return False

    """def ancestors(self, filter_condition=None):
        ancestors = self.element(by=By.XPATH, locator="./ancestor::*")
        if filter_condition is None:
            return ancestors
        return ancestors.filter(filter_condition)

    def neighbours(self, filter_condition = None):
        elements = self.element(by=By.XPATH, locator="./*")
        if filter_condition is None:
            return elements
        return elements.filter(filter_condition)"""

    def __getattr__(self, item) -> str:
        """Return value of element attribute with given name as string"""
        return self.get_attribute(item)
    
    @property
    def error_msg(self):
        return self._error_msg
    
    @error_msg.setter
    def error_msg(self, value: str):
        self._error_msg = f"{value} \n{self.error_msg}"
