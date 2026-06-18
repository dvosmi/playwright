from playwright.sync_api import Page

from ui.web_element import WebElement
from ui.page_action import PageAction


class WindowsNew:
    def __init__(self, page: Page):
        self.page = page
        self.example_text = WebElement(
            self.page.locator('//h3'),
            'example text'
        )
        self.action = PageAction(self.page)

    def get_page_text(self) -> str:
        return self.example_text.get_text_content()