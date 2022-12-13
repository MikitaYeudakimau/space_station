import uuid

import pytest

url_create_station = "http://127.0.0.1:8000/api/v1/stations/"
url_create_point = "http://127.0.0.1:8000/api/v1/stations/1/state/"


@pytest.fixture
def api_client():
    """
    Fixture for calling APIClient
    """
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def test_password():
    return 'admin'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    """
    Fixture for creating admin-user
    """

    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def login(api_client, create_user, test_password):
    """
    Fixture for admin user logging
    """
    user = create_user(
        username='admin',
        is_staff=True, is_superuser=True
    )
    api_client.login(username=user.username, password=test_password)
    return api_client, user


@pytest.fixture
def create_station(api_client):
    """
    Fixture for creation of Appollon station
    """
    response = api_client.post(url_create_station, {"name": "Apollon"})
    return response.data


@pytest.fixture
def create_right_pointing_axis_x(login):
    """
    Fixture for creating positive X movement
    """
    api_client, user = login
    data = {
        "axis": "x",
        "distance": 100,
        "user": user
    }
    api_client.post(url_create_point, data=data)
    return data


@pytest.fixture
def create_right_pointing_axis_y(login):
    """
    Fixture for creating positive Y movement
    """
    api_client, user = login
    data = {
        "axis": "y",
        "distance": 100,
        "user": user
    }
    api_client.post(url_create_point, data=data)
    return data


@pytest.fixture
def create_right_pointing_axis_z(login):
    """
    Fixture for creating positive Z movement
    """
    api_client, user = login
    data = {
        "axis": "z",
        "distance": 100,
        "user": user
    }
    api_client.post(url_create_point, data=data)
    return data


@pytest.fixture
def create_left_pointing_axis_x(login):
    """
    Fixture for creating negative X movement
    """
    api_client, user = login
    data = {
        "axis": "x",
        "distance": -200,
        "user": user
    }
    api_client.post(url_create_point, data=data)
    return data


@pytest.fixture
def create_left_pointing_axis_y(login):
    """
    Fixture for creating negative Y movement
    """
    api_client, user = login
    data = {
        "axis": "y",
        "distance": -200,
        "user": user
    }
    api_client.post(url_create_point, data=data)
    return data


@pytest.fixture
def create_left_pointing_axis_z(login):
    """
    Fixture for creating negative Z movement
    """
    api_client, user = login
    data = {
        "axis": "z",
        "distance": -200,
        "user": user
    }
    api_client.post(url_create_point, data=data)
    return data
