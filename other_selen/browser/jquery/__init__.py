from webium.driver import get_driver
from os.path import abspath

class JQuery(object):
    """ JQuery class provides jQuery wrapper for Selenium WebElement.

    Example (set element's value attr through jQuery.val function):
      e = driver.find_element_by_id('id_name')
      JQuery(e).val('New name')
    """
    JQUERY_PATH = abspath('./other_selen/browser/jquery/jquery-1.10.2.js')

    def __init__(self, browser):
        self.browser = browser
    
    
    def init(self):
        driver = self.browser.driver
        if driver.execute_script('return window.jQuery === "undefiend"'):
            with open(self.JQUERY_PATH, 'r') as jquery:
                driver.execute_script(jquery.read())
        return driver
    
    def getattr(self, name, elem):
        def jquery_func(*args):
            jquery = 'return $(arguments[0]).{func}({args});'.format(
                func=name,
                args=','.join(['arguments[%d]' % (1 + i) for i in range(len(args))])
            )
            return self.init().execute_script(jquery, elem, *args)
        return jquery_func
    
    def execute_script(self, script):
        script = [script] if isinstance(script, str) else script
        return self.init().execute_script(*script)
