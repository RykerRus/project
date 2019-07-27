
class BasePage:
    
    def __init__(self, browser) -> None:
        """
        :param Test: class driver_object Работа браузером
        """
        self.browser = browser
        self.elem = {}
    
    def switch_page(self, url: str = "") -> None:
        """
        переадрисация на другую страницу

        :param url: Гипперссылка конечной страницы
        """
        self.browser.open(url)

