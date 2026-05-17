import pytest

from page_object.login_page import LoginPage
from page_object.header_menu import HeaderMenu
from faker import Faker

from playwright.sync_api import Page

URL_HOME_PAGE = 'http://144.31.139.115:5000'

fake_eu = Faker('en_US')


@pytest.mark.parametrize('username, password', [(fake_eu.user_name(), fake_eu.password()), ])
def test_login_page(p_and_browser: Page, username: str, password: str):
    page = p_and_browser

    page.goto(URL_HOME_PAGE)

    header_menu = HeaderMenu(page)

    header_menu.redirect_login_page()

    login_page = LoginPage(page)

    login_page.login(username, password)

    assert login_page.is_submit_spinner, 'check loader visible'

    login_page.wait_for_loading()

    assert login_page.get_login_error_text() == 'Invalid login or password.', f'ER: Invalid login or password. AR: {login_page.get_login_error_text()}'
