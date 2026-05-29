from playwright.sync_api import Page


class HeaderMenu:

    def __init__(self, page: Page):
        self.page = page

        self.search_input = page.get_by_test_id('search-input')
        self.search_btn = page.get_by_test_id('search-button')

    def input_name_and_click(self, name):
        self.search_input.fill(name)
        self.search_btn.click()
