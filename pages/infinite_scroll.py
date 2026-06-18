from playwright.sync_api import Page

from ui.multi_web_element import MultiWebElement
from ui.page_action import PageAction
from ui.web_element import WebElement

# self.jscroll_added.last().evaluate('elem => elem.scrollIntoView()')

class InfiniteScroll:
    def __init__(self, page: Page):
        self.page = page
        self.jscroll_added = MultiWebElement(
            self.page.locator('//div[contains(@class, "jscroll-added")]'),
            'Paragraphs'
        )

        self.action = PageAction(self.page)

    def check_scroll_count(self) -> int:
        return self.jscroll_added.count()

    def scroll_jscroll(self) -> None:
        self.jscroll_added.last().scroll_into_view_if_needed()

