import re

from playwright.sync_api import Page
from page_object.header_menu import HeaderMenu


class SearchResults(HeaderMenu):

    def __init__(self, page: Page):
        super().__init__(page)

        self.sort_picker = page.get_by_test_id('filter-sort')
        self.apply_btn = page.get_by_test_id('apply-filters-button')
        self.loader = page.get_by_test_id('results-loader-svg')

    def wait_loader(self):
        self.loader.wait_for(state='visible')
        self.loader.wait_for(state='hidden')

    def select_filter(self, filter_type):
        self.sort_picker.select_option(filter_type)
        self.wait_loader()

    def get_search_results(self, n: int):
        results = []
        for i in range(1, n + 1):
            results.append(
                self.page.locator(f"(//div[contains(@data-testid, 'search-result-price')])[{i}]") \
                    .get_attribute('data-price'))

        return results
