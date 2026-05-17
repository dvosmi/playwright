from page_object.login_page import LoginPage
from page_object.home_page import HomePage

from playwright.sync_api import sync_playwright, Page, expect


def test_login_page(login_data):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('http://144.31.139.115:5000', wait_until='load')

        home_page = HomePage(page)

        home_page.redirect_login_page()

        login_page = LoginPage(page)

        login_page.login(*login_data)

        assert login_page.check_submit_spinner, 'check loader visible'

        login_page.wait_for_loading()

        assert login_page.get_login_error_text() == 'Invalid login or password.', 'check error text'
