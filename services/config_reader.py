import json

class ConfigReader:
    _instances = {}

    def __new__(cls, path):
        if path not in cls._instances:
            cls._instances[path] = super().__new__(cls)
        return cls._instances[path]

    def __init__(self, path):
        with open(path, 'r') as f:
            self.config = json.loads(f.read())

    def get_url(self):
        return self.config["url"]

    def get_user(self):
        username: str = self.config["user"]["username"]
        password: str = self.config["user"]["password"]
        return username, password