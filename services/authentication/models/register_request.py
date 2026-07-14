import re

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


class ValidatorConstants:
    PASSWORD_LEN_MIN = 8
    PASSWORD_LEN_MAX = 100


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    password: str = Field(
        min_length=ValidatorConstants.PASSWORD_LEN_MIN,
        max_length=ValidatorConstants.PASSWORD_LEN_MAX,
    )
    password_repeat: str
    email: EmailStr

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        password_pattern = r"""[!"#$%&'()*+,-./:;<=>?@^_`{|}~\[\]]"""
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contains at least one special character")
        if not re.search(password_pattern, value):
            raise ValueError("Password must contains at least one digit")
        return value

    @model_validator(mode="after")
    def validate_password_repeat(self):
        if self.password != self.password_repeat:
            raise ValueError("Must be equal to 'password' field")
        return self
