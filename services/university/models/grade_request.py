from pydantic import BaseModel, ConfigDict, field_validator


class GradeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    teacher_id: int
    student_id: int
    grade: int

    @field_validator("grade")
    @classmethod
    def validation_grade(cls, value):
        if not (0 <= value <= 5):
            raise ValueError("Grade must be in range of 0 to 5")
        return value
