import requests

from services.authentication.helpers.user_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def post_grade(self, data: dict) -> requests.Response:
        response = self.api_utils.post(self.ROOT_ENDPOINT, data=data)
        return response

    def get_grade(self) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT)
        return response

    def get_grade_stats(self, query) -> requests.Response:
        response = self.api_utils.get(self.ROOT_ENDPOINT + "stats/", params=query)
        return response
