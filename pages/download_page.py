from playwright.sync_api import Page

from ui.multi_web_element import MultiWebElement
from ui.page_action import PageAction
from pathlib import Path


class Download:
    def __init__(self, page: Page):
        self.page = page

        self.links = MultiWebElement(
            page.locator('//div[contains(@class, "example")]//a'),
            'link to download files'
        )
        self.action = PageAction(page)

    def get_link_text(self, number: int) -> str:
        return self.links.nth(number).get_text_content()

    def click_nth_link(self, number: int) -> None:
        self.links.nth(number).click()
