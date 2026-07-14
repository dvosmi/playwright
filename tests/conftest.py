import random

import pytest
from faker import Faker

from logger.logger import Logger
from services.authentication.authentication_service import AuthenticationService
from services.authentication.models.login_request import LoginRequest
from services.authentication.models.register_request import RegisterRequest
from services.general.models.base_grade import GradeEnum
from services.general.models.base_student import DegreeEnum
from services.general.models.base_teacher import SubjectEnum
from services.university.models.grade_request import GradeRequest
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.models.teacher_request import TeacherRequest
from services.university.university_service import UniversityService
from utils.api_utils import ApiUtils
from utils.steps.services_check_readiness import check_service_readiness

faker = Faker()


@pytest.fixture(scope="session", autouse=True)
def services_readiness():
    check_service_readiness(AuthenticationService)
    check_service_readiness(UniversityService)


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_anonym():
    api_utils = ApiUtils(url=AuthenticationService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_anonym():
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL)
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def access_token(auth_api_utils_anonym):
    auth_service = AuthenticationService(auth_api_utils_anonym)

    faker = Faker()
    username = faker.user_name()
    password = faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

    auth_service.register_user(register_request=RegisterRequest(username=username,
                                                                password=password,
                                                                password_repeat=password,
                                                                email=faker.email()))

    login_response = auth_service.login_user(login_request=LoginRequest(username=username,
                                                                        password=password))
    return login_response.access_token


@pytest.fixture(scope="function", autouse=False)
def auth_api_utils_user(access_token):
    api_utils = ApiUtils(url=AuthenticationService.SERVICE_URL, headers={"Authorization": f"Bearer {access_token}"})
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def university_api_utils_user(access_token):
    api_utils = ApiUtils(url=UniversityService.SERVICE_URL, headers={"Authorization": f"Bearer {access_token}"})
    return api_utils


@pytest.fixture(scope="function", autouse=False)
def universe_service(university_api_utils_user):
    universe_service = UniversityService(api_utils=university_api_utils_user)
    return universe_service


@pytest.fixture(scope="function", autouse=False)
def group_response(universe_service):
    Logger.info("### Create group")
    group = GroupRequest(name=faker.name())
    group_response = universe_service.create_group(group_request=group)
    return group_response


@pytest.fixture(scope="function", autouse=False)
def student_response(universe_service, group_response):
    Logger.info("### Create student")
    student = StudentRequest(first_name=faker.first_name(),
                             last_name=faker.last_name(),
                             email=faker.email(),
                             degree=random.choice([option for option in DegreeEnum]),
                             phone=faker.numerify("+79#########"),
                             group_id=group_response.id)

    student_response = universe_service.create_student(student_request=student)
    return student_response


@pytest.fixture(scope="function", autouse=False)
def teacher_response(universe_service):
    Logger.info("### Create teacher")
    teacher = TeacherRequest(first_name=faker.first_name(),
                             last_name=faker.last_name(),
                             subject=random.choice([option for option in SubjectEnum]))
    teacher_response = universe_service.create_teacher(teacher_request=teacher)
    return teacher_response


@pytest.fixture(scope="function", autouse=False)
def grade_response(universe_service, student_response, teacher_response):
    Logger.info("### Create grade")
    grade_value = random.randint(GradeEnum.GRADE_MIN, GradeEnum.GRADE_MAX)
    grade = GradeRequest(teacher_id=teacher_response.id,
                         student_id=student_response.id,
                         grade=grade_value)

    grade_response = universe_service.create_grade(grade_request=grade)
    return grade_response


@pytest.fixture(scope="function", autouse=False)
def group_factory(universe_service):
    def _group_factory():
        Logger.info("### Create group")
        group = GroupRequest(name=faker.name())
        return universe_service.create_group(group_request=group)

    return _group_factory


@pytest.fixture(scope="function", autouse=False)
def student_factory(universe_service, group_response):
    def _student_factory(group_id: int):
        Logger.info("### Create student")
        student = StudentRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 email=faker.email(),
                                 degree=random.choice([option for option in DegreeEnum]),
                                 phone=faker.numerify("+79#########"),
                                 group_id=group_id)
        return universe_service.create_student(student_request=student)

    return _student_factory


@pytest.fixture(scope="function", autouse=False)
def teacher_factory(universe_service):
    def _teacher_factory():
        Logger.info("### Create teacher")
        teacher = TeacherRequest(first_name=faker.first_name(),
                                 last_name=faker.last_name(),
                                 subject=random.choice([option for option in SubjectEnum]))
        return universe_service.create_teacher(teacher_request=teacher)

    return _teacher_factory


@pytest.fixture(scope="function", autouse=False)
def grade_factory(universe_service):
    def _grade_factory(teacher_id: int, student_id: int):
        Logger.info("### Create grade")
        grade_value = random.randint(GradeEnum.GRADE_MIN, GradeEnum.GRADE_MAX)
        grade = GradeRequest(teacher_id=teacher_id,
                             student_id=student_id,
                             grade=grade_value)
        return universe_service.create_grade(grade_request=grade)

    return _grade_factory


@pytest.fixture(scope="function", autouse=False)
def create_multi_grades(universe_service, teacher_response, student_response):
    def _create_multi_grades(count: int):
        multi_grades = []
        for _ in range(count):
            Logger.info("### Create grade")
            grade_value = random.randint(GradeEnum.GRADE_MIN, GradeEnum.GRADE_MAX)
            grade = GradeRequest(teacher_id=teacher_response.id,
                                 student_id=student_response.id,
                                 grade=grade_value)
            multi_grades.append(universe_service.create_grade(grade_request=grade))
        return multi_grades

    return _create_multi_grades


@pytest.fixture(scope="function", autouse=False)
def group_student_teacher_factory(universe_service, group_factory, student_factory, teacher_factory):
    def _group_student_teacher_factory():
        teacher = teacher_factory()
        group = group_factory()
        student = student_factory(group_id=group.id)
        return {
            "teacher": teacher,
            "group": group,
            "student": student
        }

    return _group_student_teacher_factory
