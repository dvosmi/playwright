from playwright.sync_api import Page, expect
from page_object.header_menu import HeaderMenu

class HomePage(HeaderMenu):

    def __init__(self, page: Page):
        super().__init__(page)

