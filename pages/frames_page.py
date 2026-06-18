from playwright.sync_api import Page

from ui.web_element import WebElement
from ui.page_action import PageAction


class NestedFrames:
    def __init__(self, page: Page):
        self.page = page
        self.action = PageAction(page)

        self.top_left_body = WebElement(self.page
                                        .frame_locator('//frame[contains(@name, "frame-top")]')
                                        .frame_locator('//frame[contains(@name, "frame-left")]')
                                        .locator('//body'),
                                        'frame_top_left-body'
                                        )
        self.top_right_body = WebElement(self.page
                                         .frame_locator('//frame[contains(@name, "frame-top")]')
                                         .frame_locator('//frame[contains(@name, "frame-right")]')
                                         .locator('//body'),
                                         'frame-top-right-body'
                                         )
        self.top_middle_body = WebElement(self.page
                                          .frame_locator('//frame[contains(@name, "frame-top")]')
                                          .frame_locator('//frame[contains(@name, "frame-middle")]')
                                          .locator('//body'),
                                          'frame-top-middle-body'
                                          )
        self.bottom_body = WebElement(self.page
                                      .frame_locator('//frame[contains(@name, "frame-bottom")]')
                                      .locator('//body'),
                                      'frame_bottom-body'
                                      )

    def get_top_left_body_text(self) -> str:
        return self.top_left_body.get_text_content()

    def get_top_right_body_text(self) -> str:
        return self.top_right_body.get_text_content()

    def get_top_middle_body_text(self) -> str:
        return self.top_middle_body.get_text_content()

    def get_bottom_body_text(self) -> str:
        return self.bottom_body.get_text_content()
