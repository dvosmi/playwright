import pytest

from services.authentication.helpers.user_helper import UserHelper


class TestMeContract:
    def test_me_success(self, auth_api_utils_user):
        user_helper = UserHelper(api_utils=auth_api_utils_user)

        response = user_helper.get_me()

        assert response.status_code == 200, f"Right status code. AR: '{response.status_code}', ER: '{200}'"

    @pytest.mark.xfail
    def test_me_not_authorized(self, auth_api_utils_anonym):
        user_helper = UserHelper(api_utils=auth_api_utils_anonym)

        response = user_helper.get_me()

        assert response.status_code == 401, f"Wrong status code. AR: '{response.status_code}', ER: '{401}'"
