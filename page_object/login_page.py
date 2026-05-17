from playwright.sync_api import Page, expect
from page_object.header_menu import HeaderMenu

class LoginPage(HeaderMenu):

    def __init__(self, page: Page):
        super().__init__(page)

        self.login_title = page.get_by_test_id("login-title")
        self.label_username = page.locator("//label[contains(@for, 'username')]")
        self.login_input = page.get_by_test_id("login-username")
        self.password_input = page.get_by_test_id("login-password")
        self.login_error_message = page.get_by_test_id("login-error-inline")
        self.submit_btn = page.get_by_test_id("login-submit")

        self.submit_spinner = page.get_by_test_id("login-submit-spinner")

    def is_submit_spinner(self):
        return self.submit_spinner.is_visible()

    def wait_for_loading(self):
        self.submit_spinner.wait_for(state='detached')

    def login(self, username: str, password: str):
        self.login_input.fill(username)
        self.password_input.fill(password)
        self.submit_btn.click()

    def is_login_input_edit(self):
        self.login_input.is_editable()

    def is_password_input_edit(self):
        self.password_input.is_editable()

    def is_submit_btn_enable(self):
        self.submit_btn.is_enabled()

    def is_login_error_visible(self):
        self.login_error_message.is_visible()

    def get_login_error_text(self) -> str | None:
        return self.login_error_message.text_content()

    def check_submit_class(self, css_attribute):
        return self.submit_btn.get_attribute('class') == css_attribute
