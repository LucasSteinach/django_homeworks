import pytest
from rest_framework.test import APIClient

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
def test_api_list_get(client, student):
    for i in range(0, 10):
        course = Course.objects.create(name=f'course_#{i}')
        course.students.add(student)
    courses = Course.objects.all()

    response = client.get(BASE_URL)

    assert response.status_code == 200
    # assert response.json()[:] == courses[:]
    assert len(response.json()) == 10


@pytest.mark.django_db
def test_api_filter_id(client, student):
    for i in range(10, 20):
        course = Course.objects.create(name=f'course_#{i}')
        course.students.add(student)
    response = client.get(BASE_URL + '?id=12')

    assert response.status_code == 200
    assert response.json()[0]['id'] == 12


@pytest.mark.django_db
def test_api_filter_name(client, student):
    for i in range(10, 20):
        course = Course.objects.create(name=f'course_#{i}')
        course.students.add(student)
    response = client.get(BASE_URL + '?id=12')
    courses = Course.objects.filter(id=1)

    response = client.get(BASE_URL + '?search=course_#10')

    assert response.status_code == 200
    assert response.json()[0]['name'] ==  'course_#10'


@pytest.mark.django_db
def test_api_post(client, student):
    response = client.post(BASE_URL, data={'name': 'Python', 'students': [student.id]}, format='json')

    assert response.json()['id'] == 32
    assert response.status_code == 201


@pytest.mark.django_db
def test_api_patch(client, student, course):
    new_name = 'Ultimate Python Developer'
    response = client.patch(BASE_URL + '33/', data={'name': 'Ultimate Python Developer'}, format='json')

    assert response.status_code == 200
    assert response.json()['name'] == new_name


@pytest.mark.django_db
def test_api_delete(client, student, course):

    assert client.get(BASE_URL + str(course.id) + '/').json()['id'] == course.id

    response = client.delete(f'{BASE_URL}{course.id}/')

    assert response.status_code == 204
    assert len(Course.objects.filter(id=course.id)) == 0


