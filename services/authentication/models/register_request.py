import re

from pydantic import BaseModel, ConfigDict, field_validator, model_validator, EmailStr


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    password: str
    password_repeat: str
    email: EmailStr

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password length must be longer than 7 characters.")
        if len(value) > 100:
            raise ValueError("Password length must be shorter that 100 characters.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contains at least one special character")
        if not re.search(r"[!\"#$%&\'()*+,\-./:;<=>?@^_`{|}~\[\]]", value):
            raise ValueError("Password must contains at least one digit")
        return value

    @model_validator(mode="after")
    def validate_password_repeat(self):
        if self.password != self.password_repeat:
            raise ValueError("Must be equal to 'password' field")
        return self
