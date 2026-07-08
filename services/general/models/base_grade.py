from enum import IntEnum

from pydantic import BaseModel, ConfigDict, field_validator, Field


class GradeEnum(IntEnum):
    GRADE_MIN = 0
    GRADE_MAX = 5


class BaseGrade(BaseModel):
    model_config = ConfigDict(extra="forbid")

    teacher_id: int
    student_id: int
    grade: int = Field(
        ge=GradeEnum.GRADE_MIN,
        le=GradeEnum.GRADE_MAX,
    )
