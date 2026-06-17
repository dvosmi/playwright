from playwright.sync_api import Page

from ui.multi_web_element import MultiWebElement
from ui.page_action import PageAction


class Hovers:
    def __init__(self, page: Page):
        self.page = page
        self.figures = MultiWebElement(
            self.page.locator('//div[contains(@class, "figure")]'),
            'elements user img'
        )
        self.name_user = MultiWebElement(
            self.page.locator('//h5[contains(text(), "name: user")]'),
            'some text'
        )
        self.action = PageAction(self.page)

    def get_content_nth(self, index: int) -> str:
        return self.name_user.nth(index).get_text_content()

    def generate_content_figures(self):
        for index, element in enumerate(self.figures.all()):
            element.hover()
            yield self.get_content_nth(index), index + 1
