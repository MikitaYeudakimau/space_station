import uuid

import pytest

from django.urls import reverse


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


@pytest.fixture(scope='function')
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
    url = reverse("space-list")
    response = api_client.post(url, {"name": "Apollon"})
    return response.data


@pytest.fixture
def create_right_pointing_axis_x(create_station, login):
    """
    Fixture for creating positive X movement
    """
    station_data = create_station
    api_client, user = login
    request_data = {
        "axis": "x",
        "distance": 100,
        "user": user
    }
    url = reverse("space-detail-state", kwargs={'pk': station_data['id']})
    api_client.post(url, data=request_data)
    return station_data, request_data


@pytest.fixture
def create_right_pointing_axis_y(create_station, login):
    """
    Fixture for creating positive Y movement
    """
    station_data = create_station
    api_client, user = login
    request_data = {
        "axis": "y",
        "distance": 100,
        "user": user
    }
    url = reverse("space-detail-state", kwargs={'pk': station_data['id']})
    api_client.post(url, data=request_data)
    return station_data, request_data


@pytest.fixture
def create_right_pointing_axis_z(create_station, login):
    """
    Fixture for creating positive Z movement
    """
    station_data = create_station
    api_client, user = login
    request_data = {
        "axis": "z",
        "distance": 100,
        "user": user
    }
    url = reverse("space-detail-state", kwargs={'pk': station_data['id']})
    api_client.post(url, data=request_data)
    return station_data, request_data


@pytest.fixture
def create_left_pointing_axis_x(create_station, login):
    """
    Fixture for creating negative X movement
    """
    station_data = create_station
    api_client, user = login
    request_data = {
        "axis": "x",
        "distance": -200,
        "user": user
    }
    url = reverse("space-detail-state", kwargs={'pk': station_data['id']})
    api_client.post(url, data=request_data)
    return station_data, request_data


@pytest.fixture
def create_left_pointing_axis_y(create_station, login):
    """
    Fixture for creating negative Y movement
    """
    station_data = create_station
    api_client, user = login
    request_data = {
        "axis": "y",
        "distance": -200,
        "user": user
    }
    url = reverse("space-detail-state", kwargs={'pk': station_data['id']})
    api_client.post(url, data=request_data)
    return station_data, request_data


@pytest.fixture
def create_left_pointing_axis_z(create_station, login):
    """
    Fixture for creating negative Z movement
    """
    station_data = create_station
    api_client, user = login
    request_data = {
        "axis": "z",
        "distance": -200,
        "user": user
    }
    url = reverse("space-detail-state", kwargs={'pk': station_data['id']})
    api_client.post(url, data=request_data)
    return station_data, request_data
