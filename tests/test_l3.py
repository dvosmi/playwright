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
        basic_auth = BasicAuth(page_auth)

        basic_auth.action.goto('https://the-internet.herokuapp.com/basic_auth')

        content_p_text = basic_auth.get_content_p_text()
        assert content_p_text == 'Congratulations! You must have the proper credentials.', \
            f'ER: "Congratulations! You must have the proper credentials.". AR: "{content_p_text}"'

    def test_alerts(self, page: Page, random_text: str) -> None:
        alerts = Alerts(page)

        alerts.action.goto('https://the-internet.herokuapp.com/javascript_alerts')

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
        context_menu = ContextMenu(page)

        context_menu.action.goto('https://the-internet.herokuapp.com/context_menu')

        context_alert = context_menu.accept_alert()
        assert context_alert == 'You selected a context menu', \
            f'ER: "You selected a context menu". AR: {context_alert}'

    def test_slider(self, page: Page, random_number: int) -> None:
        horizontal_slider = HorizontalSlider(page)

        horizontal_slider.action.goto('https://the-internet.herokuapp.com/horizontal_slider')

        horizontal_slider.press_slider_right(random_number)

        expect_value = random_number * 0.5
        slider_value = horizontal_slider.get_slider_value()
        assert slider_value == expect_value, f'ER: "{slider_value}". AR: "{expect_value}"'

    def test_hover(self, page: Page) -> None:
        hovers = Hovers(page)

        hovers.action.goto('https://the-internet.herokuapp.com/hovers')

        for index, element in enumerate(hovers.figures.all()):
            element.hover()

            assert hovers.get_content_nth(index) == f'name: user{index + 1}'

    def test_windows(self, page: Page) -> None:
        windows = Windows(page)

        windows.action.goto('https://the-internet.herokuapp.com/windows')

        page_new = windows.open_new_page()

        page_new_action = PageAction(page_new)
        page_new_windows = WindowsNew(page_new)
        page_new.bring_to_front()
        page_new_text = page_new_windows.get_page_text()

        assert page_new_text == 'New Window', f'ER: "New Window". AR: {page_new_text}'

        page.bring_to_front()

        page_new2 = windows.open_new_page()

        page_new2_action = PageAction(page_new2)
        page_new2_windows = WindowsNew(page_new2)
        page_new2.bring_to_front()
        page_new2_text = page_new2_windows.get_page_text()

        assert page_new2_text == 'New Window', f'ER: "New Window". AR: {page_new2_text}'

        page.bring_to_front()

        page_new_action.close_page()
        page_new2_action.close_page()

        pages = page.context.pages

        assert len(pages) == 1, f'ER: 1. AR: {len(pages)}'

    def test_frames(self, page: Page):
        frames = NestedFrames(page)

        frames.action.goto('https://the-internet.herokuapp.com/nested_frames')

        top_left_text = frames.get_top_left_body_text()
        assert top_left_text == 'LEFT', f'ER: "LEFT". AR: {top_left_text}'

        top_right_text = frames.get_top_right_body_text()
        assert top_right_text == 'RIGHT', f'ER: "RIGHT". AR: {top_right_text}'

        bottom_text = frames.get_bottom_body_text()
        assert bottom_text == 'BOTTOM', f'ER: "RIGHT". AR: {bottom_text}'

        top_middle_text = frames.get_top_middle_body_text()
        assert top_middle_text == 'MIDDLE', f'ER: "RIGHT". AR: {top_middle_text}'

    def test_dynamic_content(self, page: Page):
        dynamic_content = DynamicContent(page)

        dynamic_content.action.goto('https://the-internet.herokuapp.com/dynamic_content')

        while True:
            try:
                assert dynamic_content.check_imgs_match(), 'ER: True'
                break
            except AssertionError:
                dynamic_content.reload_page()

    def test_scroll(self, page: Page):
        scroll = InfiniteScroll(page)

        scroll.action.goto('https://the-internet.herokuapp.com/infinite_scroll')

        while True:
            try:
                assert scroll.check_jscroll_count() >= 10, 'Success'
                break
            except AssertionError:
                scroll.scrolling()

    def test_upload_image(self, page: Page, file_name: str):
        upload = Upload(page)

        upload.action.goto('https://the-internet.herokuapp.com/upload')

        upload.upload_file(file_name)
        upload_text = upload.get_upload_text()
        uploaded_file_text = upload.get_uploaded_file_text()

        assert upload_text == 'File Uploaded!', f'ER: "File Uploaded!". AR: {upload_text}'
        assert uploaded_file_text == file_name, f'ER: {file_name}. AR: {uploaded_file_text}'

    def test_download(self, page: Page, link_number: int):
        downland = Download(page)

        downland.action.goto('https://the-internet.herokuapp.com/download')

        link_name = downland.get_link_text(link_number)
        downland.download_file(link_number)

        assert downland.check_download_filename(link_name), 'ER: True'

        downland.delete_download_file(link_name)