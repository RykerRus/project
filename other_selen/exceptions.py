from selenium.common.exceptions import WebDriverException


class NoRunBrowserException(WebDriverException):
    def __init__(self, message="message: No run browser."):\
        self.message = message
        
    def __str__(self):
        return self.message
    