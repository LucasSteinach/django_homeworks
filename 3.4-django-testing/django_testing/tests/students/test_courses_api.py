import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course


BASE_URL = '/api/v1/courses/'
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student():
    return Student.objects.create(name='Pupkin')

@pytest.fixture
def course(student):
    course = Course.objects.create(name='Python')
    course.students.add(student)
    return course

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


# @pytest.mark.django_db
# def test_function(fixtures):
    #  Arrange
    #  Act
    #  Assert

@pytest.mark.django_db
def test_api_retrieve_get(client, student, course):
    response = client.get(BASE_URL + '1/')

    assert response.json()['id'] == 1
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_list_get(client, student, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(BASE_URL)


    assert response.status_code == 200
    assert len(response.json()) == len(courses)
    for i, cours in enumerate(response.json()):
        assert cours['name'] == courses[i].name

@pytest.mark.django_db
def test_api_filter_id(client, student, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(BASE_URL + f'?id={courses[3].id}')

    assert response.status_code == 200
    assert response.json()[0]['id'] == courses[3].id


@pytest.mark.django_db
def test_api_filter_name(client, student, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(BASE_URL + f'?search={courses[3].name}')

    assert response.status_code == 200
    assert response.json()[0]['name'] == courses[3].name


@pytest.mark.django_db
def test_api_post(client, student):
    response = client.post(BASE_URL, data={'name': 'Python', 'students': [student.id]})

    assert response.json()['id'] == 32
    assert response.status_code == 201


@pytest.mark.django_db
def test_api_patch(client, student, course, course_factory):
    data = {'name': 'Ultimate Python Developer'}
    cours = course_factory(_quantity=1)
    response = client.patch(BASE_URL + str(cours[0].id) + '/', data={'name': 'Ultimate Python Developer'})

    assert response.status_code == 200
    assert response.json()['name'] == data['name']


@pytest.mark.django_db
def test_api_delete(client, student, course):
    assert client.get(BASE_URL + str(course.id) + '/').json()['id'] == course.id

    response = client.delete(f'{BASE_URL}{course.id}/')

    assert response.status_code == 204
    assert len(Course.objects.filter(id=course.id)) == 0


