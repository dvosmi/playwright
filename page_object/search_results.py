from playwright.sync_api import Page
from page_object.header_menu import HeaderMenu


class SearchResults(HeaderMenu):

    def __init__(self, page: Page):
        super().__init__(page)

        self.sort_picker = page.get_by_test_id('filter-sort')
        self.apply_btn = page.get_by_test_id('apply-filters-button')
        self.loader = page.get_by_test_id('results-loader-svg')

        self.results = []

    def wait_loader(self):
        self.loader.wait_for(state='visible')
        self.loader.wait_for(state='hidden')

    def select_filter(self, filter_type):
        self.sort_picker.select_option(filter_type)
        self.wait_loader()

    def get_search_results(self, n: int):
        for i in range(1, n + 1):
            self.results.append(self.page.get_by_test_id("search-results-grid").locator(f"(//article)[{i}]") \
                                .locator("//div[contains(@class, 'article-price')]").get_attribute('data-price'))
        return self.results

    def check_filter_price(self, n: int, filter_type: str):
        self.get_search_results(n)
        if filter_type == 'Price: low to high':
            for i in range(1, len(self.results)):
                if self.results[i] < self.results[i - 1]:
                    return False
            else:
                return True
        elif filter_type == 'Price: high to low':
            for i in range(1, len(self.results)):
                if self.results[i] > self.results[i - 1]:
                    return False
            else:
                return True
        pass
