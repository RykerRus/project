import pytest

from ..browser import Browser
from .element import Element

@pytest.fixture(scope="session")
def herokuapp_url():
    """Return site test server base URL"""
    return "https://the-internet.herokuapp.com"

@pytest.fixture(scope="session")
def pikabu_url(scope="module"):
    return "https://pikabu.ru"


@pytest.yield_fixture()
def browser():
    browser_ = Browser()
    yield browser_
    browser_.close_all_windows()
    