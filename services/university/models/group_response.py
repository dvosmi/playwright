from pydantic import BaseModel, ConfigDict


class GroupResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    id: int
