from pydantic import BaseModel, ConfigDict, EmailStr


class StudentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str
    last_name: str
    email: EmailStr
    degree: str
    phone: str
    group_id: int
    id: int
