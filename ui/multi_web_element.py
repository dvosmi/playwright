from playwright.sync_api import Page, Locator
from typing_extensions import Self

from ui.web_element import WebElement


class MultiWebElement:
    def __init__(self,
                 locator: Locator,
                 description: str,
                 page: Page | None = None
                 ) -> None:
        self.page = page
        self.locator = locator
        self.description = description
        self.index = 0

    def __iter__(self) -> Self:
        self.index = 0
        return self

    def __next__(self) -> WebElement:
        if self.index >= self.locator.count():
            raise StopIteration

        element = WebElement(
            locator=self.locator.nth(self.index),
            description=f'{self.description}[{self.index}]'
        )

        self.index += 1
        return element

    def __str__(self) -> str:
        return f'MultiWebElement[{self.description}]'

    def nth(self, index: int) -> WebElement:
        return WebElement(
            locator=self.locator.nth(index),
            description=f'{self.description}[{index}]'
        )

    def first(self) -> WebElement:
        return WebElement(
            locator=self.locator.first,
            description=f'{self.description}[first]'
        )

    def last(self) -> WebElement:
        return WebElement(
            locator=self.locator.last,
            description=f'{self.description}[last]'
        )

    def count(self) -> int:
        return self.locator.count()

    def all(self) -> list[WebElement]:
        return [
            WebElement(
                locator=loc,
                description=f'{self.description}[{i}]'
            ) for i, loc in enumerate(self.locator.all())
        ]
