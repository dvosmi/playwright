import json

from playwright.sync_api import Browser, BrowserContext, Page


class PageFactory:

    def __init__(self, browser: Browser) -> None:
        self.browser = browser

    def create_page(self, http_credentials=None) -> Page:
        context = self._create_context(http_credentials)
        page = context.new_page()

        return page

    def _create_context(self, http_credentials) -> BrowserContext:
        context = self.browser.new_context(
            http_credentials=http_credentials
        )

        return context
