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

    def click_link(self) -> None:
        self.click_here_link.click()
