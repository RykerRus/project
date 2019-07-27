from .page.personal import Personal
from .page.profile import Profile

from .config import browsers

import pytest, mimesis

class TestRegistration:
    _NAME = "Регистрация"
    
    @pytest.mark.parametrize("capabilities", browsers)
    def test_registration_true(self, browser: "class Browser", capabilities, domain):
        self.browser = browser
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = Personal(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.open_reg_form()
        login = mimesis.Person().password(length=12)
        password = mimesis.Person().password(length=12)
        page.registration(login=login, password=password, password_confirm=password)
        if not browser.debug:
            btn = page.registration_sumbit()
            btn.hover()
            btn.click()
            assert btn.hidden(wait=5), "Ошибка Клика: После клика не сработало событие регистрации и кнопка не пропала"
            
            page_profile = Profile(browser)
            page_profile.open()
            assert page_profile.sumbit().visible(), "Ошибка: Подтверждения регистрации"

    @pytest.mark.parametrize("capabilities", browsers)
    def test_registration_false1(self, browser: "class Browser", capabilities, domain):
        """
        Проверка валидации:
        login: Короткое имя
        pass: короткий пороль
        confirm pass: Пароль отличный от поля pass
        
        """
        self.browser = browser
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} не корректный ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = Personal(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.open_reg_form()

        page.registration(login="ts", password="123", password_confirm="123456")
        if not browser.debug:
            btn = page.registration_sumbit()
            btn.hover()
            btn.click()
            assert btn.visible(wait=5), ("Ошибка: Кнопка подтверждения регистрации пропала."
                                         "Вероятно регистрация с некоректными данными успешна")
            error = page.get_registration_error()
            result = ""
            if "Логин должен быть не менее 3 символов." not in error:
                result += "Не найдена ошибка о коротком имени \n"
            if "Пароль должен быть не менее 6 символов длиной." not in error:
                result += "Не найдена ошибка о коротком пароле \n"
            if "Неверное подтверждение пароля." not in error:
                result += "Не найдена ошибка о не совпадение паролей \n"
            assert "" == result, result + error

    @pytest.mark.parametrize("capabilities", browsers)
    def test_registration_false2(self, browser: "class Browser", capabilities, domain):
        """
        Проверка валидации:
        login: Короткое имя
        pass: короткий пороль
        confirm pass: Пароль отличный от поля pass

        """
        self.browser = browser
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} попытка регистрации на занятый логин браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = Personal(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.open_reg_form()
        password = mimesis.Person().password(length=12)
        page.registration(login="test", password=password, password_confirm=password)
        if not browser.debug:
            btn = page.registration_sumbit()
            btn.hover()
            btn.click()
            assert btn.visible(wait=5), ("Ошибка: Кнопка подтверждения регистрации пропала."
                                         "Вероятно регистрация с некоректными данными успешна")
            error = page.get_registration_error()
            assert 'Пользователь с логином "test" уже существует.' == error

    @pytest.mark.parametrize("capabilities", browsers)
    def test_registration_false(self, browser: "class Browser", capabilities, domain):
        """
        Проверка валидации:
        login: Короткое имя
        pass: короткий пороль
        confirm pass: Пароль отличный от поля pass

        """
        self.browser = browser
        string = f"{capabilities[1]}, версия {capabilities[0]['version']}"
        browser.data["name"] = f"{self._NAME} пустой ввод браузер {capabilities[0]['browserName']} {string}"
        browser.setup_browser(capabilities[0]["browserName"], remote=True, desired_capabilities=capabilities[0])
        page = Personal(browser)
        page.open()
        browser.driver.set_window_size(1920, 1080)
        page.open_reg_form()
    
        if not browser.debug:
            btn = page.registration_sumbit()
            btn.hover()
            btn.click()
            assert btn.visible(wait=5), ("Ошибка: Кнопка подтверждения регистрации пропала."
                                         "Вероятно регистрация с некоректными данными успешна")
            error = page.get_registration_error()
            result = ""
            if 'Поле "Логин (мин. 3 символа)" обязательно для заполнения' not in error:
                result += "Не найдена ошибка о обязательном поле имя"
            if 'Поле "Пароль" обязательно для заполнения' not in error:
                result += "Не найдена ошибка о обязательном поле пароль"
            if 'Поле "Подтверждение пароля" обязательно для заполнения' not in error:
                result += "Не найдена ошибка о обязательном поле подтверждения пароля"
            assert "" == result, result