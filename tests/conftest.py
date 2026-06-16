import pytest
from faker import Faker

from playwright.sync_api import sync_playwright

from logger import setup_logger
from services.config_reader import ConfigReader

from services.page_factory import PageFactory


@pytest.fixture(scope="session", autouse=True)
def init_logger():
    setup_logger()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser


@pytest.fixture(scope='function')
def page(browser):
    new_page = PageFactory(browser)
    yield new_page.create_page()


@pytest.fixture(scope='function')
def page_auth(browser):
    CONFIG_PATH = 'tests/data/basic_authorization_data.json'
    config = ConfigReader(CONFIG_PATH)
    username, password = config.get_user()

    new_page = PageFactory(browser)
    yield new_page.create_page(
        http_credentials={
            "username": username,
            "password": password,
        }
    )


@pytest.fixture(scope='function')
def random_text():
    fake = Faker()
    random_text = fake.text(max_nb_chars=30)
    yield random_text


@pytest.fixture(scope='function')
def link_number():
    link_number = 3
    yield link_number
