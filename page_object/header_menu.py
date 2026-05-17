from playwright.sync_api import Page, expect

class HeaderMenu:

    def __init__(self, page: Page):
        self.page = page

        self.login_btn = page.get_by_test_id("nav-login")

    def redirect_login_page(self):
        self.login_btn.click()
        self.page.wait_for_url("**/login")

