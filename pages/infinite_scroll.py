from playwright.sync_api import Page

from ui.multi_web_element import MultiWebElement
from ui.page_action import PageAction


class InfiniteScroll:
    def __init__(self, page: Page):
        self.page = page
        self.jscroll_added = MultiWebElement(
            page.locator('//div[contains(@class, "jscroll-added")]'),
            'Paragraphs'
        )
        self.action = PageAction(self.page)

    def check_jscroll_count(self) -> int:
        return self.jscroll_added.count()

    def scrolling(self) -> None:
        self.action.evaluate('window.scrollTo(0, document.body.scrollHeight)')