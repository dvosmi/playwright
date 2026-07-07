from enum import IntEnum

from pydantic import BaseModel, ConfigDict, field_validator


class GradeEnum(IntEnum):
    GRADE_MIN = 0
    GRADE_MAX = 5


class BaseGrade(BaseModel):
    model_config = ConfigDict(extra="forbid")

    teacher_id: int
    student_id: int
    grade: int

    @field_validator("grade")
    @classmethod
    def validation_grade(cls, value):
        if not (GradeEnum.GRADE_MIN <= value <= GradeEnum.GRADE_MAX):
            raise ValueError(f"Grade must be in range of {GradeEnum.GRADE_MIN} to {GradeEnum.GRADE_MAX}")
        return value