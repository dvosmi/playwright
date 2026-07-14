import time

import requests


def check_service_readiness(service):
    timeout = 60
    start_time = time.time()
    while time.time() < start_time + timeout:
        try:
            response = requests.get(service.SERVICE_URL + "/docs")
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        else:
            break
    else:
        raise RuntimeError(f"'{service}' service wasn't started during '{timeout}' second.")
