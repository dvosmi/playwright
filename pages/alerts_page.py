from playwright.sync_api import Page

from ui.web_element import WebElement
from ui.page_action import PageAction

class Alerts:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.js_alert_btn = WebElement(
            self.page.locator('//button[contains(@onclick, "jsAlert()")]'),
            'Button "Click for JS Alert"',
        )
        self.js_confirm_btn = WebElement(
            self.page.locator('//button[contains(@onclick, "jsConfirm()")]'),
            'Button "Click for JS Confirm"',
        )
        self.js_prompt_btn = WebElement(
            self.page.locator('//button[contains(@onclick, "jsPrompt()")]'),
            'Button "Click for JS Prompt"',
        )
        self.text_result = WebElement(
            self.page.locator(f'//*[contains(@id, "result")]'),
            "Result text"
        )
        self.action = PageAction(self.page)


    def get_alert_message(self) -> str:
        return self.action.accept_alert(self.js_alert_btn.click)

    def get_confirm_message(self) -> str:
        return self.action.accept_alert(self.js_confirm_btn.click)

    def get_prompt_message(self, random_text: str) -> str:
        return self.action.accept_prompt(self.js_prompt_btn.click, random_text)

    def get_text_result(self) -> str:
        return self.text_result.get_text_content()
