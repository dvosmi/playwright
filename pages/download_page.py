from playwright.sync_api import Page

from ui.multi_web_element import MultiWebElement
from ui.page_action import PageAction
from pathlib import Path


class Download:
    def __init__(self, page: Page):
        self.page = page

        self.links = MultiWebElement(
            page.locator('//div[contains(@class, "example")]//a'),
            'link to download files'
        )
        self.action = PageAction(page)

    def get_link_text(self, number: int) -> str:
        return self.links.nth(number - 1).get_text_content()

    def _get_file_value(self, number: int):
        with self.page.expect_download() as download_info:
            self.links.nth(number - 1).click()
        file_value = download_info.value
        return file_value

    def get_name_file(self, number: int) -> str:
        file = self._get_file_value(number)
        return file.suggested_filename

    def download_file(self, number: int) -> None:
        file = self._get_file_value(number)
        file_name = file.suggested_filename
        file.save_as(file_name)

    def check_download_filename(self, filename: str) -> bool:
        return Path(filename).is_file()

    def delete_download_file(self, filename: str) -> None:
        file = Path(filename)
        file.unlink()