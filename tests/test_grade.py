from faker import Faker
from faker.generator import random

from logger.logger import Logger
from services.university.models.grade_request import GradeRequest
from services.university.models.grade_statistic_query_request import GradeStatisticQueryRequest

faker = Faker()


class TestGrade:
    def test_grade_create(self, universe_service, student_response, teacher_response):
        Logger.info("### Create grade")

        grade_value = random.randint(0, 5)
        grade = GradeRequest(teacher_id=teacher_response.id,
                             student_id=student_response.id,
                             grade=grade_value)
        grade_response = universe_service.create_grade(grade_request=grade)

        assert grade_response.teacher_id == teacher_response.id, f"Right teacher id. \
                    AR: '{teacher_response.id}', ER: '{grade_response.teacher_id}'"
        assert grade_response.student_id == student_response.id, f"Right teacher id. \
                    AR: '{student_response.id}', ER: '{grade_response.student_id}'"
        assert grade_response.grade == grade_value, f"Right teacher id. \
                    AR: '{grade_value}', ER: '{grade_response.grade}'"

    def test_get_grade(self, universe_service, grade_response):
        Logger.info("### Get Grade")

        get_grade_response = universe_service.get_grade()

        assert any(grade_response.model_dump().items() <= item.model_dump().items()
                   for item in get_grade_response), f"Created grade is return in Get request, \
                   AR: Get request list {get_grade_response} not contains '{grade_response}', \
                   ER: Get request list contains '{grade_response}'"

    def test_get_grade_stats(self, universe_service, create_multi_grades):
        Logger.info('### Get Grade Stats')

        count = 10
        multi_grades = create_multi_grades(count)
        grades_grade = [grades.grade for grades in multi_grades]
        grade_min = min(grades_grade),
        grade_max = max(grades_grade),
        grade_avg = sum(grades_grade) / len(multi_grades)

        get_grade_response = universe_service.get_grade_stats()

        assert get_grade_response.count == count, f"Get stat count, \
            AR: {get_grade_response.count}, ER: {count}"
        assert get_grade_response.min == grade_min, f"Get stats min, \
            AR: {get_grade_response.min}, ER: {grade_min}"
        assert get_grade_response.max == grade_max, f"Get stats max, \
            AR: {get_grade_response.max}, ER: {grade_max}"
        assert get_grade_response.avg == grade_avg, f"Get stats avg, \
            AR: {get_grade_response.max}, ER: {grade_avg}"

    def test_get_grade_stats_teacher(self, universe_service, group_factory, student_factory, teacher_factory,
                                     grade_factory):
        teacher_1 = teacher_factory()
        teacher_2 = teacher_factory()
        group = group_factory()
        student = student_factory(group_id=group.id)
        grade_factory(teacher_id=teacher_1.id, student_id=student.id)
        count = 3
        multi_grades = [grade_factory(teacher_id=teacher_2.id, student_id=student.id) for _ in range(count)]
        expected_grade = universe_service.calculate_expect_grade_stats(multi_grades=multi_grades)

        get_grade_response = universe_service.get_grade_stats(
            query_params=GradeStatisticQueryRequest(teacher_id=teacher_2.id))

        assert get_grade_response.count == count, f"Get stat count, \
            AR: {get_grade_response.count}, ER: {count}"
        assert get_grade_response.min == expected_grade["min"], f"Get stats min, \
            AR: {get_grade_response.min}, ER: {expected_grade["min"]}"
        assert get_grade_response.max == expected_grade["max"], f"Get stats max, \
            AR: {get_grade_response.max}, ER: {expected_grade["max"]}"
        assert get_grade_response.avg == expected_grade["avg"], f"Get stats avg, \
            AR: {get_grade_response.max}, ER: {expected_grade["avg"]}"

    def test_get_grade_stats_student(self, universe_service, group_factory, student_factory, teacher_factory,
                                     grade_factory):
        teacher = teacher_factory()
        group = group_factory()
        student_1 = student_factory(group_id=group.id)
        student_2 = student_factory(group_id=group.id)
        grade_factory(teacher_id=teacher.id, student_id=student_1.id)
        count = 3
        multi_grades = [grade_factory(teacher_id=teacher.id, student_id=student_2.id) for _ in range(count)]
        expected_grade = universe_service.calculate_expect_grade_stats(multi_grades=multi_grades)

        get_grade_response = universe_service.get_grade_stats(
            query_params=GradeStatisticQueryRequest(student_id=student_2.id))

        assert get_grade_response.count == count, f"Get stat count, \
            AR: {get_grade_response.count}, ER: {count}"
        assert get_grade_response.min == expected_grade["min"], f"Get stats min, \
            AR: {get_grade_response.min}, ER: {expected_grade["min"]}"
        assert get_grade_response.max == expected_grade["max"], f"Get stats max, \
            AR: {get_grade_response.max}, ER: {expected_grade["max"]}"
        assert get_grade_response.avg == expected_grade["avg"], f"Get stats avg, \
            AR: {get_grade_response.max}, ER: {expected_grade["avg"]}"

    def test_get_grade_stats_group(self, universe_service, group_factory, student_factory, teacher_factory,
                                   grade_factory):
        teacher = teacher_factory()
        group_1 = group_factory()
        group_2 = group_factory()
        student_1 = student_factory(group_id=group_1.id)
        student_2 = student_factory(group_id=group_2.id)
        grade_factory(teacher_id=teacher.id, student_id=student_1.id)
        count = 3
        multi_grades = [grade_factory(teacher_id=teacher.id, student_id=student_2.id) for _ in range(count)]
        expected_grade = universe_service.calculate_expect_grade_stats(multi_grades=multi_grades)

        get_grade_response = universe_service.get_grade_stats(
            query_params=GradeStatisticQueryRequest(student_id=student_2.id))

        assert get_grade_response.count == count, f"Get stat count, \
                    AR: {get_grade_response.count}, ER: {count}"
        assert get_grade_response.min == expected_grade["min"], f"Get stats min, \
                    AR: {get_grade_response.min}, ER: {expected_grade["min"]}"
        assert get_grade_response.max == expected_grade["max"], f"Get stats max, \
                    AR: {get_grade_response.max}, ER: {expected_grade["max"]}"
        assert get_grade_response.avg == expected_grade["avg"], f"Get stats avg, \
                    AR: {get_grade_response.max}, ER: {expected_grade["avg"]}"
