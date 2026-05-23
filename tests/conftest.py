import pytest
from playwright.sync_api import sync_playwright
import json


class ConfigReader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            with open('config.json', 'r') as f:
                self.config = json.load(f)
            self.initialized = True

    def get_url(self):
        return self.config["url"]


@pytest.fixture(scope='session')
def p_and_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser.new_page()
