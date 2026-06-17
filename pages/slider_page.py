from playwright.sync_api import Page

from ui.web_element import WebElement
from ui.page_action import PageAction

import random


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
        random_value = random_number // 5

        for _ in range(random_value):
            self.action.keyboard_press('ArrowRight')

    def get_slider_value(self) -> float:
        return float(self.slider_number.get_text_content())

    def get_min_value(self) -> float:
        min_value = float(self.slider.get_attribute('min'))
        return min_value

    def get_max_value(self) -> float:
        max_value = float(self.slider.get_attribute('max'))
        return max_value

    def get_step_value(self) -> float:
        step_value = float(self.slider.get_attribute('step'))
        return step_value
