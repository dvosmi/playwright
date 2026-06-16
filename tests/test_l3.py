from pathlib import Path
import tempfile

from services.config_reader import ConfigReader
from playwright.sync_api import Page
from ui.page_action import PageAction

from pages.basic_auth_page import BasicAuth
from pages.alerts_page import Alerts
from pages.context_menu_page import ContextMenu
from pages.slider_page import HorizontalSlider
from pages.hovers_page import Hovers
from pages.windows.windows_page import Windows
from pages.windows.windows_new_page import WindowsNew
from pages.frames_page import NestedFrames
from pages.dynamic_content_page import DynamicContent
from pages.infinite_scroll import InfiniteScroll
from pages.upload_page import Upload
from pages.download_page import Download


class TestClass:
    def test_basic_authorization(self, page_auth: Page) -> None:
        CONFIG_PATH = 'tests/data/basic_authorization_data.json'
        config = ConfigReader(CONFIG_PATH)

        basic_auth = BasicAuth(page_auth)

        basic_auth.action.goto(config.get_url())

        content_p_text = basic_auth.get_content_p_text()
        assert content_p_text == 'Congratulations! You must have the proper credentials.', \
            f'ER: "Congratulations! You must have the proper credentials.". AR: "{content_p_text}"'

    def test_alerts(self, page: Page, random_text: str) -> None:
        CONFIG_PATH = 'tests/data/alerts_data.json'
        config = ConfigReader(CONFIG_PATH)

        alerts = Alerts(page)

        alerts.action.goto(config.get_url())

        js_alert = alerts.get_alert_message()
        assert js_alert == 'I am a JS Alert', f'ER: "I am a JS Alert". AR: {js_alert}'

        result_js_alert = alerts.get_text_result()
        assert result_js_alert == 'You successfully clicked an alert', \
            f'ER: "You successfully clicked an alert". AR: {result_js_alert}'

        js_confirm = alerts.get_confirm_message()
        assert js_confirm == 'I am a JS Confirm', f'ER: "I am a JS Confirm". AR: {js_confirm}'

        result_js_confirm = alerts.get_text_result()
        assert result_js_confirm == 'You clicked: Ok', f'ER: "You clicked: Ok". AR: {result_js_confirm}'

        js_prompt = alerts.get_prompt_message(random_text)
        assert js_prompt == 'I am a JS prompt', f'ER: "I am a JS prompt". AR: {js_prompt}'

        result_js_prompt = alerts.get_text_result()
        assert result_js_prompt == f'You entered: {random_text}', \
            f'ER: "You entered: {random_text}". AR: {result_js_prompt}'

    def test_context_click(self, page: Page) -> None:
        CONFIG_PATH = 'tests/data/context_click_data.json'
        config = ConfigReader(CONFIG_PATH)

        context_menu = ContextMenu(page)

        context_menu.action.goto(config.get_url())

        context_alert = context_menu.accept_alert()
        assert context_alert == 'You selected a context menu', \
            f'ER: "You selected a context menu". AR: {context_alert}'

    def test_slider(self, page: Page) -> None:
        CONFIG_PATH = 'tests/data/slider_data.json'
        config = ConfigReader(CONFIG_PATH)

        horizontal_slider = HorizontalSlider(page)

        horizontal_slider.action.goto(config.get_url())
        random_number = horizontal_slider.get_random_value()

        horizontal_slider.press_slider_right(random_number)

        expect_value = random_number / 10
        slider_value = horizontal_slider.get_slider_value()
        assert slider_value == expect_value, f'ER: "{slider_value}". AR: "{expect_value}"'

    def test_hover(self, page: Page) -> None:
        CONFIG_PATH = 'tests/data/hover_data.json'
        config = ConfigReader(CONFIG_PATH)

        hovers = Hovers(page)

        hovers.action.goto(config.get_url())

        for content, index in hovers.generate_content_figures():
            assert content == f'name: user{index}', f'ER: "user{index}". AR: "{content}"'

    def test_windows(self, page: Page) -> None:
        CONFIG_PATH = 'tests/data/windows_data.json'
        config = ConfigReader(CONFIG_PATH)

        windows = Windows(page)

        windows.action.goto(config.get_url())

        with windows.action.expect_new_page() as new_page_info:
            windows.click_link()

        page_new = new_page_info.value

        page_new_action = PageAction(page_new)
        page_new_windows = WindowsNew(page_new)
        page_new.bring_to_front()
        page_new_text = page_new_windows.get_page_text()

        assert page_new_text == 'New Window', f'ER: "New Window". AR: "{page_new_text}"'

        page.bring_to_front()

        with windows.action.expect_new_page() as new_page_info:
            windows.click_link()

        page_new2 = new_page_info.value

        page_new2_action = PageAction(page_new2)
        page_new2_windows = WindowsNew(page_new2)
        page_new2.bring_to_front()
        page_new2_text = page_new2_windows.get_page_text()

        assert page_new2_text == 'New Window', f'ER: "New Window". AR: "{page_new2_text}"'

        page.bring_to_front()

        page_new_action.close_page()
        page_new2_action.close_page()

        pages = page.context.pages

        assert len(pages) == 1, f'ER: 1. AR: {len(pages)}'

    def test_frames(self, page: Page):
        CONFIG_PATH = 'tests/data/frames_data.json'
        config = ConfigReader(CONFIG_PATH)

        frames = NestedFrames(page)

        frames.action.goto(config.get_url())

        top_left_text = frames.get_top_left_body_text()
        assert top_left_text == 'LEFT', f'ER: "LEFT". AR: "{top_left_text}"'

        top_right_text = frames.get_top_right_body_text()
        assert top_right_text == 'RIGHT', f'ER: "RIGHT". AR: "{top_right_text}"'

        bottom_text = frames.get_bottom_body_text()
        assert bottom_text == 'BOTTOM', f'ER: "RIGHT". AR: "{bottom_text}"'

        top_middle_text = frames.get_top_middle_body_text()
        assert top_middle_text == 'MIDDLE', f'ER: "RIGHT". AR: "{top_middle_text}"'

    def test_dynamic_content(self, page: Page):
        CONFIG_PATH = 'tests/data/dynamic_content_data.json'
        config = ConfigReader(CONFIG_PATH)

        dynamic_content = DynamicContent(page)

        dynamic_content.action.goto(config.get_url())

        while True:
            try:
                img_match = dynamic_content.check_imgs_match()
                assert img_match, f'ER: "True". AR: "{img_match}"'
                break
            except AssertionError:
                dynamic_content.action.reload_page()

    def test_scroll(self, page: Page):
        CONFIG_PATH = 'tests/data/scroll_data.json'
        config = ConfigReader(CONFIG_PATH)

        scroll = InfiniteScroll(page)

        scroll.action.goto(config.get_url())

        while True:
            try:
                scroll_count = scroll.check_scroll_count()
                assert scroll_count >= 10, f'ER: "10". AR: "{scroll_count}"'
                break
            except AssertionError:
                scroll.scroll_jscroll()

    def test_upload_image(self, page: Page):
        CONFIG_PATH = 'tests/data/upload_image_data.json'
        config = ConfigReader(CONFIG_PATH)

        upload = Upload(page)

        upload.action.goto(config.get_url())

        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        tmp_file_path = Path(tmp_file.name)
        tmp_file_name = tmp_file_path.name

        upload.upload_file(tmp_file_path)
        upload_text = upload.get_upload_text()
        uploaded_file_text = upload.get_uploaded_file_text()

        assert upload_text == 'File Uploaded!', f'ER: "File Uploaded!". AR: "{upload_text}"'
        assert uploaded_file_text == tmp_file_name, f'ER: "{tmp_file_name}". AR: "{uploaded_file_text}"'

        tmp_file.close()
        tmp_file_path.unlink(missing_ok=True)

    def test_download(self, page: Page, link_number: int):
        CONFIG_PATH = 'tests/data/download_data.json'
        config = ConfigReader(CONFIG_PATH)

        downland = Download(page)

        downland.action.goto(config.get_url())

        with downland.action.expect_download() as download_info:
            downland.click_nth_link(link_number-1)
        file_value = download_info.value
        file_name = file_value.suggested_filename
        file_value.save_as(file_name)

        link_name = downland.get_link_text(link_number-1)

        downland_filename = Path(link_name).is_file()
        assert downland_filename, f'ER: "{file_name}". AR: "{downland_filename}"'

        file = Path(link_name)
        file.unlink()
