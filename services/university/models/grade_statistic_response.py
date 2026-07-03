from pydantic import BaseModel, ConfigDict, field_validator


class GradeStatisticResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    count: int
    min: int | None = None
    max: int | None = None
    avg: float | None = None

    @field_validator("count")
    @classmethod
    def validation_count(cls, count):
        if count < 0:
            raise ValueError("Count must be >= 0")
        return count