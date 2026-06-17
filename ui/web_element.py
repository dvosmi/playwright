import logging

from playwright.sync_api import Page, Locator

from logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class WebElement:
    def __init__(self,
                 locator: Locator,
                 description: str,
                 page: Page | None = None,
                 ) -> None:
        self.page = page
        self.locator = locator
        self.description = description

    def __str__(self) -> str:
        return f'WebElement[{self.description}]'

    def get_text_content(self) -> str:
        logger.info(f'{self}: get text content')
        result = self.locator.text_content().strip()
        logger.info(f'{self}: text content = "{result}"')
        return result

    def click(self) -> None:
        logger.info(f'{self}: click')
        self.locator.click()

    def right_click(self) -> None:
        logger.info(f'{self}: right_click')
        self.locator.click(button='right')

    def focus(self) -> None:
        logger.info(f'{self}: focus')
        self.locator.focus()

    def get_attribute(self, attribute: str) -> str:
        logger.info(f'{self}: get_attribute "{attribute}"')
        result = self.locator.get_attribute(attribute)
        logger.info(f'{self}: attribute "{attribute}" = "{result}"')
        return result

    def press(self, key: str) -> None:
        logger.info(f'{self}: press "{key}"')
        self.locator.press(key)

    def hover(self) -> None:
        logger.info(f'{self}: hover')
        self.locator.hover()

    def is_visible(self) -> bool:
        logger.info(f'{self}: is visible')
        return self.locator.is_visible()

    def set_input_files(self, file: str) -> None:
        logger.info(f'{self}: upload file {file}')
        return self.locator.set_input_files(file)

    def evaluate(self, command) -> None:
        logger.info(f'{self}: evaluate {command}')
        self.locator.evaluate(f'{command}')

    def scroll_into_view_if_needed(self) -> None:
        logger.info(f'{self}: scroll_into_view_if_needed()')
        self.locator.scroll_into_view_if_needed()