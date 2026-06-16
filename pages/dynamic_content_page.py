from playwright.sync_api import Page

from ui.multi_web_element import MultiWebElement
from ui.page_action import PageAction


class DynamicContent:
    def __init__(self, page: Page):
        self.page = page

        self.avatar_imgs = MultiWebElement(
            self.page.locator("//img"),
            'avatar_imgs'
        )
        self.action = PageAction(self.page)

    def check_imgs_match(self) -> bool:
        set_avatar_imgs = set()
        for img in self.avatar_imgs:
            set_avatar_imgs.add(img.get_attribute('src'))
        return self.avatar_imgs.count() != len(set_avatar_imgs)
