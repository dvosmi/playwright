from playwright.sync_api import Page

from ui.web_element import WebElement
from ui.page_action import PageAction


class Upload:

    def __init__(self, page: Page):
        self.page = page

        self.file_upload = WebElement(
            page.locator('//input[contains(@id, "file-upload")]'),
            'Upload file locator'
        )
        self.upload_btn = WebElement(
            page.locator('//input[contains(@id, "file-submit")]'),
            'Upload button',
        )
        self.file_upload_text = WebElement(
            page.locator('//div[contains(@class, "example")]//h3'),
            'File Uploaded! after reload page'
        )
        self.uploaded_files = WebElement(
            page.locator('//div[contains(@id, "uploaded-files")]'),
            'Name uploaded files',
        )
        self.action = PageAction(self.page)

    def upload_file(self, file) -> None:
        self.file_upload.set_input_files(file)
        self.upload_btn.click()
        self.action.wait_for_load_state('load')

    def get_upload_text(self) -> str:
        return self.file_upload_text.get_text_content()

    def get_uploaded_file_text(self) -> str:
        return self.uploaded_files.get_text_content()