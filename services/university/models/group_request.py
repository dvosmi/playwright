from pydantic import BaseModel, ConfigDict


class GroupRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
