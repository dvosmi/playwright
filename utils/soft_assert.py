class SoftAssert:
    def __init__(self):
        self.errors = []

    def assert_equal(self, actual, expected, message):
        if actual != expected:
            self.errors.append(
                f"{actual!r} != {expected!r}, {message}"
            )

    def assert_all(self):
        if self.errors:
            raise AssertionError("\n".join(self.errors))
