import pytest
from playwright.sync_api import sync_playwright
from page_object.search_results import SearchResults
from page_object.header_menu import HeaderMenu
from playwright.sync_api import Page
from service.config_reader import ConfigReader
from service.enum_sort_filter import FilterSort as Sort

CONFIG_PATH = 'config.json'

config = ConfigReader(CONFIG_PATH)


@pytest.mark.parametrize('n, filter_type', [(10, Sort.LOW_TO_HIGH), (15, Sort.HIGH_TO_LOW)])
@pytest.mark.parametrize('name', ['city', 'habits'])
def test_sort_filter(page: Page, name, n, filter_type):
    page.goto(config.get_url())

    header_menu = HeaderMenu(page)

    header_menu.input_name_and_click(name)

    search_result = SearchResults(page)

    search_result.wait_loader()
    search_result.select_filter(filter_type)

    results = search_result.get_search_results(n)

    if filter_type == Sort.LOW_TO_HIGH:
        assert (results == sorted(results)), f'Name:{name}; n: {n}; filter_type: {filter_type}'
    elif filter_type == Sort.HIGH_TO_LOW:
        assert (results == sorted(results, reverse=True)), f'Name:{name}; n: {n}; filter_type: {filter_type}'
