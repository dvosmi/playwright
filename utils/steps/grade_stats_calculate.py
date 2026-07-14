from services.university.models.grade_statistic_response import GradeStatisticResponse


def grade_stats_calculate(multi_grades: list):
    grade = [g.grade for g in multi_grades]
    count = len(grade)

    return GradeStatisticResponse(count=count, min=min(grade), max=max(grade), avg=sum(grade) / count)
