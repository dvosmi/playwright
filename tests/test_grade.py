import pytest_check as check
from faker import Faker
from faker.generator import random

from logger.logger import Logger
from services.general.models.base_grade import GradeEnum
from services.university.models.grade_request import GradeRequest
from utils.steps.grade_stats_assert import grade_stats_assert
from utils.steps.grade_stats_calculate import grade_stats_calculate

faker = Faker()


class TestGrade:
    def test_grade_create(self, universe_service, student_response, teacher_response):
        Logger.info("### Create grade")

        grade_value = random.randint(GradeEnum.GRADE_MIN, GradeEnum.GRADE_MAX)
        grade = GradeRequest(teacher_id=teacher_response.id,
                             student_id=student_response.id,
                             grade=grade_value)
        grade_response = universe_service.create_grade(grade_request=grade)

        check.equal(grade_response.teacher_id,
                    teacher_response.id,
                    f"Wrong teacher id. AR: '{teacher_response.id}', ER: '{grade_response.teacher_id}'")

        check.equal(grade_response.student_id,
                    student_response.id,
                    f"Wrong teacher id. AR: '{student_response.id}', ER: '{grade_response.student_id}'")

        check.equal(grade_response.grade,
                    grade_value,
                    f"Wrong teacher id. AR: '{grade_value}', ER: '{grade_response.grade}'")

    def test_get_grade(self, universe_service, grade_response):
        Logger.info("### Get Grade")

        get_grade_response = universe_service.get_grade()

        assert any(grade_response.model_dump().items() <= item.model_dump().items()
                   for item in get_grade_response), f"Get request return wrong grade, \
                   AR: Get request list {get_grade_response} not contains '{grade_response}', \
                   ER: Get request list contains '{grade_response}'"

    def test_get_grade_stats(self, universe_service, create_multi_grades):
        Logger.info('### Get Grade Stats')

        count = 9
        create_multi_grades(count)
        multi_grades = universe_service.get_grade()
        expected_grade = grade_stats_calculate(multi_grades=multi_grades)

        get_grade_response = universe_service.get_grade_stats()

        grade_stats_assert(get_grade_response, expected_grade)

    def test_get_grade_stats_group(self, universe_service, group_student_teacher_factory, grade_factory):
        group_student_teacher_1 = group_student_teacher_factory()
        group_student_teacher_2 = group_student_teacher_factory()

        grade_factory(teacher_id=group_student_teacher_1["teacher"].id,
                      student_id=group_student_teacher_1["student"].id)
        count = 3
        multi_grades = [grade_factory(teacher_id=group_student_teacher_1["teacher"].id,
                                      student_id=group_student_teacher_2["student"].id) for _ in range(count)]
        expected_grade = grade_stats_calculate(multi_grades=multi_grades)

        get_grade_response = universe_service.get_grade_stats(group_id=group_student_teacher_2["group"].id)

        grade_stats_assert(get_grade_response, expected_grade)

    def test_get_grade_stats_student(self, universe_service, group_student_teacher_factory, grade_factory):
        group_student_teacher_1 = group_student_teacher_factory()
        group_student_teacher_2 = group_student_teacher_factory()

        grade_factory(teacher_id=group_student_teacher_1["teacher"].id,
                      student_id=group_student_teacher_1["student"].id)
        count = 3
        multi_grades = [grade_factory(teacher_id=group_student_teacher_1["teacher"].id,
                                      student_id=group_student_teacher_2["student"].id) for _ in range(count)]
        expected_grade = grade_stats_calculate(multi_grades=multi_grades)

        get_grade_response = universe_service.get_grade_stats(student_id=group_student_teacher_2["student"].id)

        grade_stats_assert(get_grade_response, expected_grade)

    def test_get_grade_stats_teacher(self, universe_service, group_student_teacher_factory, grade_factory):
        group_student_teacher_1 = group_student_teacher_factory()
        group_student_teacher_2 = group_student_teacher_factory()

        grade_factory(teacher_id=group_student_teacher_1["teacher"].id,
                      student_id=group_student_teacher_1["student"].id)
        count = 3
        multi_grades = [grade_factory(teacher_id=group_student_teacher_2["teacher"].id,
                                      student_id=group_student_teacher_1["student"].id) for _ in range(count)]
        expected_grade = grade_stats_calculate(multi_grades=multi_grades)

        get_grade_response = universe_service.get_grade_stats(teacher_id=group_student_teacher_2["teacher"].id)

        grade_stats_assert(get_grade_response, expected_grade)
