import pytest

from page_object.search_results import SearchResults
from page_object.header_menu import HeaderMenu
from playwright.sync_api import Page, sync_playwright
from tests.conftest import ConfigReader

config = ConfigReader()


@pytest.mark.parametrize('name, n, filter_type', [
    ('city', 10, 'Price: low to high'),
    ('city', 15, 'Price: high to low'),
    ('habits', 10, 'Price: low to high'),
    ('habits', 15, 'Price: high to low')
])
def test_sort_filter(p_and_browser: Page, name, n, filter_type):
    page = p_and_browser

    page.goto(config.get_url())

    header_menu = HeaderMenu(page)

    header_menu.input_name_and_click(name)

    search_result = SearchResults(page)

    search_result.wait_loader()
    search_result.select_filter(filter_type)

    assert (search_result.check_filter_price(n, filter_type)), f'Name:{name}; n: {n}; filter_type: {filter_type}'
