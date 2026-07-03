import requests
from faker import Faker

from services.authentication.helpers.authorization_helper import AuthorizationHelper
from services.authentication.helpers.user_helper import UserHelper
from utils.api_utils import ApiUtils

AUTH_DATA = "http://127.0.0.1:8000"

REGISTER_ENDPOINT = "/auth/register/"
LOGIN_ENDPOINT = "/auth/login/"

faker = Faker()

username = faker.user_name()
password = faker.word() + "1sdlf!"

authorization_helper = AuthorizationHelper(api_utils=ApiUtils(AUTH_DATA))

response = authorization_helper.post_register(data={"username": username,
                                                    "password": password,
                                                    "password_repeat": password,
                                                    "email": faker.email()})

response = authorization_helper.post_login(data={"username": username,
                                                 "password": password})

access_token = response.json()["access_token"]

user_auth_helper = UserHelper(api_utils=ApiUtils(AUTH_DATA, headers={"Authorization": f"Bearer {access_token}"}))

response = user_auth_helper.get_me()
print(response)