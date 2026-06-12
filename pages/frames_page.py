from playwright.sync_api import Page

from ui.web_element import WebElement
from ui.page_action import PageAction


class NestedFrames:
    def __init__(self, page: Page):
        self.page = page

        self.frame_top = page.frame_locator('//frame[contains(@name, "frame-top")]')
        self.frame_bottom = page.frame_locator('//frame[contains(@name, "frame-bottom")]')
        self.action = PageAction(page)

    @property
    def frame_top_left(self):
        return self.frame_top.frame_locator('//frame[contains(@name, "frame-left")]')

    @property
    def frame_top_right(self):
        return self.frame_top.frame_locator('//frame[contains(@name, "frame-right")]')

    @property
    def frame_top_middle(self):
        return self.frame_top.frame_locator('//frame[contains(@name, "frame-middle")]')

    @property
    def top_left_body(self):
        return WebElement(
            self.frame_top_left.locator('//body'),
            'locator-frame_top_left-body'
        )

    @property
    def top_right_body(self):
        return WebElement(
            self.frame_top_right.locator('//body'),
            'locator-frame_top_right-body'
        )

    @property
    def top_middle_body(self):
        return WebElement(
            self.frame_top_middle.locator('//body'),
            'locator-frame_top_middle-body'
        )

    @property
    def bottom_body(self):
        return WebElement(
            self.frame_bottom.locator('//body'),
            'locator-frame_bottom-body'
        )

    def get_top_left_body_text(self) -> str:
        return self.top_left_body.get_text_content()

    def get_top_right_body_text(self) -> str:
        return self.top_right_body.get_text_content()

    def get_top_middle_body_text(self) -> str:
        return self.top_middle_body.get_text_content()

    def get_bottom_body_text(self) -> str:
        return self.bottom_body.get_text_content()
