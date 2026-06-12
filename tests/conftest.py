import pytest
from playwright.sync_api import sync_playwright

from logger import setup_logger
from faker import Faker

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
    new_page = PageFactory(browser)
    yield new_page.create_page(
        http_credentials={
            "username": "admin",
            "password": "admin"
        }
    )


@pytest.fixture(scope='function')
def random_text():
    fake = Faker()
    random_text = fake.text(max_nb_chars=30)
    yield random_text


@pytest.fixture(scope='function')
def random_number():
    fake = Faker()
    random_number = fake.random_int(min=1, max=9)
    yield random_number


@pytest.fixture(scope='function')
def file_name():
    file_name = 'upload_image_file'
    yield file_name


@pytest.fixture(scope='function')
def link_number():
    link_number = 3
    yield link_number
