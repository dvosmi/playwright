import pytest

from page_object.search_results import SearchResults
from page_object.header_menu import HeaderMenu
from playwright.sync_api import Page
from service.config_reader import ConfigReader
from service.enum_sort_filter import FilterSort as Sort

CONFIG_PATH = 'config.json'

config = ConfigReader(CONFIG_PATH)


@pytest.mark.parametrize('name', ['city', 'habits'])
@pytest.mark.parametrize('n', [10, 15])
@pytest.mark.parametrize('filter_type', [Sort.LOW_TO_HIGH, Sort.HIGH_TO_LOW])
def test_sort_filter(page: Page, name, n, filter_type):
    page.goto(config.get_url())

    header_menu = HeaderMenu(page)

    header_menu.input_name_and_click(name)

    search_result = SearchResults(page)

    search_result.wait_loader()
    search_result.select_filter(filter_type)

    results = search_result.get_search_results(n)

    if filter_type == 'Price: low to high':
        assert (results == sorted(results)), f'Name:{name}; n: {n}; filter_type: {filter_type}'
    elif filter_type == 'Price: high to low':
        assert (results == sorted(results, reverse=True)), f'Name:{name}; n: {n}; filter_type: {filter_type}'
