from pydantic import BaseModel, ConfigDict

class GradeStatisticQueryRequest(BaseModel):

    student_id: int | None = None
    teacher_id: int | None = None
    group_id: int | None = None
