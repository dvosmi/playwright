from playwright.sync_api import Page

from ui.web_element import WebElement
from ui.page_action import PageAction

class ContextMenu:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.hot_spot = WebElement(
            self.page.locator('//div[contains(@id, "hot-spot")]'),
            'area within',
        )
        self.action = PageAction(page)

    def accept_alert(self) -> str:
        area_click = self.hot_spot.right_click
        return self.action.accept_alert(area_click)