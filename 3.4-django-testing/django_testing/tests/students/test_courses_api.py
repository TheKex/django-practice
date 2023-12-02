import pytest
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient

from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, make_m2m=True, *args, **kwargs)

    return factory


@pytest.fixture
def course(courses_factory):
    return courses_factory(_quantity=1)[0]


@pytest.mark.django_db
def test_get_course(client, course):
    resp = client.get(f"/api/v1/courses/{course.id}/")
    assert resp.status_code == HTTP_200_OK
    resp_course_name = resp.json().get('name')
    assert resp_course_name == course.name


@pytest.mark.django_db
def test_get_courses(client, courses_factory):
    course_list = courses_factory(_quantity=10)
    resp = client.get("/api/v1/courses/")
    assert resp.status_code == HTTP_200_OK
    resp_course_list = resp.json()
    assert len(resp_course_list) == len(course_list)
    for index, course in enumerate(course_list):
        assert course.name == resp_course_list[index]['name']


@pytest.mark.django_db
def test_filter_course_by_id(client, courses_factory):
    course_list = courses_factory(_quantity=10)
    resp = client.get("/api/v1/courses/", data={"id": course_list[0].id}, format="json")
    assert resp.status_code == HTTP_200_OK
    assert len(resp.json()) == 1
    resp_course_name = resp.json()[0].get('name')
    assert resp_course_name == course_list[0].name


@pytest.mark.django_db
def test_filter_course_by_name(client, courses_factory):
    course_list = courses_factory(_quantity=10)
    resp = client.get("/api/v1/courses/", data={"name": course_list[0].name}, format="json")
    assert resp.status_code == HTTP_200_OK
    resp_course_name = resp.json()[0].get('name')
    assert resp_course_name == course_list[0].name


@pytest.mark.django_db
def test_create_course(client, students_factory):
    students = students_factory(_quantity=3)
    course = {
        "name": "test course",
        "students": [student.id for student in students]
    }
    resp = client.post("/api/v1/courses/", data=course, format="json")
    assert resp.status_code == HTTP_201_CREATED
    assert resp.json().get('name') == course['name']
    assert len(resp.json().get('students')) == len(students)


@pytest.mark.django_db
def test_update_course(client, course, students_factory):
    student = students_factory(_quantity=1)[0]
    update_course_data = {
        "name": "new name",
        "students": [student.id]
    }
    resp = client.patch(f'/api/v1/courses/{course.id}/',
                        data=update_course_data,
                        format='json')
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json['name'] == update_course_data['name']
    assert resp_json['students'][0] == student.id


@pytest.mark.django_db
def test_delete_course(client, course):
    resp = client.delete(f'/api/v1/courses/{course.id}/')
    assert resp.status_code == HTTP_204_NO_CONTENT
    db_courses_count = Course.objects.filter(id=course.id).count()
    assert db_courses_count == 0
