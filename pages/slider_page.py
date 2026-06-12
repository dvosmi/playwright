from playwright.sync_api import Page

from ui.web_element import WebElement
from ui.page_action import PageAction

class HorizontalSlider:
    def __init__(self, page: Page):
        self.page = page
        self.slider = WebElement(
            self.page.locator('//input[contains(@type, "range")]'),
            'slider',
        )
        self.slider_number = WebElement(
            self.page.locator('//span[contains(@id, "range")]'),
            'slider number'
        )
        self.action = PageAction(self.page)

    def press_slider_right(self, random_number: int) -> None:
        self.slider.focus()

        for _ in range(random_number):
            self.action.keyboard_press('ArrowRight')

    def get_slider_value(self) -> float:
        return float(self.slider_number.get_text_content())