from faker import Faker

from services.authentication.helpers.authorization_helper import AuthorizationHelper

faker = Faker()


class TestRegisterContract:
    def test_login_success(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        password = faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        username = faker.user_name()

        response = auth_helper.post_register(
            data={"username": username, "password": password, "password_repeat": password, "email": faker.email()}
        )

        response = auth_helper.post_login(data={"username": username, "password": password})

        assert response.status_code == 200, f"Wrong status code. AR: '{response.status_code}', ER: '{200}'"

    def test_validation_login_wrong(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        response = auth_helper.post_login(data={"username": None, "password": None})

        assert response.status_code == 422, f"Wrong status code. AR: '{response.status_code}', ER: '{422}'"

    def test_invalid_login_wrong(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        response = auth_helper.post_login(data={"username": faker.user_name(), "password": faker.word()})

        assert response.status_code == 401, f"Wrong status code. AR: '{response.status_code}', ER: '{401}'"
