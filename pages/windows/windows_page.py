from playwright.sync_api import Page

from ui.web_element import WebElement
from ui.page_action import PageAction


class Windows:
    def __init__(self, page: Page):
        self.page = page
        self.click_here_link = WebElement(
            self.page.locator('//a[contains(@href, "/windows/new")]'),
            'link "Click here"'
        )
        self.action = PageAction(page)

    def open_new_page(self):
        with self.action.expect_new_page() as new_page_info:
            self.click_here_link.click()
        new_page = new_page_info.value
        new_page.wait_for_load_state('load')
        return new_page
