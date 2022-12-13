import uuid

import pytest

from django.urls import reverse

url_create_point = "http://127.0.0.1:8000/api/v1/stations/1/state/"

from space import models
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
def create_right_pointing_axis_x(create_station,login):
    """
    Fixture for creating positive X movement
    """
    station_data = create_station
    api_client, user = login
    data = {
        "axis": "x",
        "distance": 100,
        "user": user
    }
    url = reverse("space-detail-state",kwargs={'pk':station_data['id']})
    api_client.post(url_create_point, data=data)
    return station_data, data


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

@pytest.mark.django_db
def test_create_station(create_station):
    """
    Test creation of station
    """
    station_name = create_station['name']
    assert models.SpaceStation.objects.count() == 1
    assert models.SpaceStation.objects.first().name == station_name


@pytest.mark.django_db
def test_right_pointing_axis_x(create_right_pointing_axis_x):
    """
    Test creation of point with positive X direction
    """
    station_data, pointing = create_right_pointing_axis_x
    assert models.Pointing.objects.count() == 1
    assert models.Pointing.objects.first().axis == pointing["axis"]
    assert models.Pointing.objects.first().distance == pointing["distance"]


@pytest.mark.django_db
def test_movement_station_axis_x(create_station, create_right_pointing_axis_x):
    """
    Test change of station X-coordinate
    """
    start_position_x = create_station['position_x']
    pointing = create_right_pointing_axis_x
    assert start_position_x + pointing['distance'] == 200


@pytest.mark.django_db
def test_right_pointing_axis_y(create_station, create_right_pointing_axis_y):
    """
    Test creation of point with positive Y direction
    """
    pointing = create_right_pointing_axis_y
    assert models.Pointing.objects.count() == 1
    assert models.Pointing.objects.first().axis == pointing["axis"]
    assert models.Pointing.objects.first().distance == pointing["distance"]


@pytest.mark.django_db
def test_movement_station_axis_y(create_station, create_right_pointing_axis_y):
    """
    Test change of station Y-coordinate
    """
    start_position_x = create_station['position_y']
    pointing = create_right_pointing_axis_y
    assert start_position_x + pointing['distance'] == 200


@pytest.mark.django_db
def test_right_pointing_axis_z(create_station, create_right_pointing_axis_z):
    """
    Test creation of point with positive Z direction
    """
    pointing = create_right_pointing_axis_z
    assert models.Pointing.objects.count() == 1
    assert models.Pointing.objects.first().axis == pointing["axis"]
    assert models.Pointing.objects.first().distance == pointing["distance"]


@pytest.mark.django_db
def test_movement_station_axis_z(create_station, create_right_pointing_axis_z):
    """
    Test change of station Z-coordinate
    """
    start_position_x = create_station['position_z']
    pointing = create_right_pointing_axis_z
    assert start_position_x + pointing['distance'] == 200


@pytest.mark.django_db
def test_station_condition_before_pointing(create_station):
    """
    Check station status after creation
    """
    station_condition = create_station['condition']
    assert station_condition == "running"


@pytest.mark.django_db
def test_station_condition_after_right_pointing_axis_x(create_station, create_right_pointing_axis_x):
    """
    Check station status after right X movement
    """
    station_name = create_station['name']
    station = models.SpaceStation.objects.get(name=station_name)
    assert station.condition == "running"


@pytest.mark.django_db
def test_station_condition_after_left_pointing_axis_x(create_station, create_left_pointing_axis_x):
    """
    Check station status after left X movement
    """
    station_name = create_station['name']
    station = models.SpaceStation.objects.get(name=station_name)
    assert station.condition == "broken"
