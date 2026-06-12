from playwright.sync_api import Page

from ui.multi_web_element import MultiWebElement
from ui.page_action import PageAction


class DynamicContent:
    def __init__(self, page: Page):
        self.page = page

        self.imgs = MultiWebElement(
            self.page.locator("//img"),
            'imgs'
        )
        self.action = PageAction(self.page)

    def check_imgs_match(self) -> bool:
        set_imgs = set()
        for img in self.imgs:
            set_imgs.add(img.get_attribute('src'))
        return self.imgs.count() != len(set_imgs)

    def reload_page(self) -> None:
        self.action.reload_page()