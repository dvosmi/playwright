from playwright.sync_api import Dialog, Page
from collections.abc import Callable
import logging
from logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class PageAction:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, url: str) -> None:
        logger.info(f'PageAction: goto "{url}"')
        self.page.goto(url)

    def _handle_dialog(
            self,
            action: Callable[[], None],
            mode: str,
            prompt_text: str | None = None
    ) -> str:
        logger.info('PageAction: expect dialog')
        message = ''

        def handle_dialog(dialog: Dialog) -> None:
            nonlocal message
            message = dialog.message
            logger.info(f'PageAction: dialog "{dialog.type}" with message "{message}"')
            if mode == 'dismiss':
                dialog.dismiss()
                return

            if prompt_text is None:
                dialog.accept()
                return

            dialog.accept(prompt_text)

        self.page.once('dialog', handle_dialog)
        action()

        if not message:
            raise RuntimeError('Expected dialog was not shown')

        return message

    def accept_alert(self, action: Callable[[], None]) -> str:
        logger.info('PageAction: accept dialog')
        return self._handle_dialog(action, mode='accept')

    def accept_prompt(self, action: Callable[[], None], prompt_text: str) -> str:
        logger.info('PageAction: accept prompt')
        return self._handle_dialog(action, mode='accept', prompt_text=prompt_text)

    def keyboard_press(self, key: str) -> None:
        logger.info(f'PageAction: keyboard press "{key}"')
        self.page.keyboard.press(key)

    def expect_new_page(self):
        logger.info('PageAction: expect new page')
        return self.page.context.expect_page()

    def close_page(self) -> None:
        logger.info(f'PageAction: close page')
        self.page.close()

    def bring_to_front(self) -> None:
        logger.info(f'PageAction: bring page to front')
        self.page.bring_to_front()

    def wait_for_load_state(self, state: str | None = None) -> None:
        logger.info(f'PageAction: wait for load state "state"')
        self.page.wait_for_load_state(state)

    def reload_page(self) -> None:
        logger.info(f'PageAction: reload page')
        self.page.reload()

    def evaluate(self, command) -> None:
        logger.info(f'PageAction: ScrollTo')
        self.page.evaluate(f'{command}')