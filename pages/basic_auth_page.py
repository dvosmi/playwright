from playwright.sync_api import Page

from ui.web_element import WebElement
from ui.page_action import PageAction


class BasicAuth:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.content_p_text = WebElement(
            self.page.locator('(//div[contains(@id, "content")]//p)'),
            "visible text after authorization",
        )
        self.action = PageAction(self.page)

    def get_content_p_text(self) -> str:
        return self.content_p_text.get_text_content()