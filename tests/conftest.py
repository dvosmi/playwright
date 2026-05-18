import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope='session')
def p_and_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser.new_page()
