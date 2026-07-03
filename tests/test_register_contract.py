import requests
from faker import Faker

from services.authentication.helpers.authorization_helper import AuthorizationHelper

faker = Faker()


class TestRegisterContract:
    def test_register_success(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        password = faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

        response = auth_helper.post_register(data={
            "username": faker.user_name(),
            "password": password,
            "password_repeat": password,
            "email": faker.email()})

        assert response.status_code == requests.status_codes.codes.created, f"Right status code. \
        AR: '{response.status_code}', ER: '{requests.status_codes.codes.created}'"

    def test_register_wrong_username(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        password = faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

        response = auth_helper.post_register(data={"username": None,
                                                   "password": password,
                                                   "password_repeat": password,
                                                   "email": faker.email()})

        assert response.status_code == 422, f"Wrong status code. AR: '{response.status_code}', ER: '{422}'"

    def test_register_wrong_none_password(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        response = auth_helper.post_register(data={
            "username": faker.user_name(),
            "password": None,
            "password_repeat": None,
            "email": faker.email()})

        assert response.status_code == 422, f"Wrong status code. AR: '{response.status_code}', ER: '{422}'"

    def test_register_wrong_shorter_password(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        password = faker.password(length=7, special_chars=True, digits=True, upper_case=True, lower_case=True)

        response = auth_helper.post_register(data={
            "username": faker.user_name(),
            "password": password,
            "password_repeat": password,
            "email": faker.email()})

        assert response.status_code == 422, f"Wrong status code. AR: '{response.status_code}', ER: '{422}'"

    def test_register_wrong_longer_password(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        password = faker.password(length=101, special_chars=True, digits=True, upper_case=True, lower_case=True)

        response = auth_helper.post_register(data={
            "username": faker.user_name(),
            "password": password,
            "password_repeat": password,
            "email": faker.email()})

        assert response.status_code == 422, f"Wrong status code. AR: '{response.status_code}', ER: '{422}'"

    def test_register_wrong_longer_password(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        password = faker.password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)

        response = auth_helper.post_register(data={
            "username": faker.user_name(),
            "password": password,
            "password_repeat": password,
            "email": faker.email()})

        assert response.status_code == 422, f"Wrong status code. AR: '{response.status_code}', ER: '{422}'"

    def test_register_wrong_longer_password(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        password = faker.password(length=10, special_chars=True, digits=False, upper_case=True, lower_case=True)

        response = auth_helper.post_register(data={
            "username": faker.user_name(),
            "password": password,
            "password_repeat": password,
            "email": faker.email()})

        assert response.status_code == 422, f"Wrong status code. AR: '{response.status_code}', ER: '{422}'"

    def test_register_wrong_password_repeat(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        password = faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

        response = auth_helper.post_register(data={
            "username": faker.user_name(),
            "password": password,
            "password_repeat": None,
            "email": faker.email()})

        assert response.status_code == 422, f"Wrong status code. AR: '{response.status_code}', ER: '{422}'"

    def test_register_wrong_email(self, auth_api_utils_anonym):
        auth_helper = AuthorizationHelper(api_utils=auth_api_utils_anonym)

        password = faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

        response = auth_helper.post_register(data={
            "username": faker.user_name(),
            "password": password,
            "password_repeat": password,
            "email": None})

        assert response.status_code == 422, f"Wrong status code. AR: '{response.status_code}', ER: '{422}'"
