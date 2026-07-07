from pydantic import BaseModel, ConfigDict, model_validator


class GradeStatisticQueryRequest(BaseModel):
    student_id: int | None = None
    teacher_id: int | None = None
    group_id: int | None = None

    @model_validator(mode="after")
    def validate_null(self):
        for field in ("student_id", "teacher_id", "group_id"):
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
            return self
