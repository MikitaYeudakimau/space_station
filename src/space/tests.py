import uuid

import pytest

from space import models

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
    created_station_name = response.data['name']
    return created_station_name


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
def create_right_pointing_axis_y(create_user):
    user = create_user()
    pointing = models.Pointing.objects.create(axis="y", distance=200, user=user)
    return pointing


@pytest.fixture
def create_right_pointing_axis_z(create_user):
    user = create_user()
    pointing = models.Pointing.objects.create(axis="z", distance=300, user=user)
    return pointing


@pytest.fixture
def create_left_pointing_axis_x(create_user):
    user = create_user()
    pointing = models.Pointing.objects.create(axis="x", distance=-100, user=user)
    return pointing


@pytest.fixture
def create_left_pointing_axis_y(create_user):
    user = create_user()
    pointing = models.Pointing.objects.create(axis="y", distance=-200, user=user)
    return pointing


@pytest.fixture
def create_left_pointing_axis_z(create_user):
    user = create_user()
    pointing = models.Pointing.objects.create(axis="z", distance=-300, user=user)
    return pointing


@pytest.mark.django_db
def test_create_station(create_station):
    """
    Test creation of station
    """
    station_name = create_station
    assert models.SpaceStation.objects.count() == 1
    assert models.SpaceStation.objects.first().name == station_name


@pytest.mark.django_db
def test_right_pointing_axis_x(create_station,create_right_pointing_axis_x):
    """
    Test creation of point with positive X direction
    """
    create_station
    pointing = create_right_pointing_axis_x
    assert models.Pointing.objects.count() == 1
    assert models.Pointing.objects.first().axis == pointing["axis"]
    assert models.Pointing.objects.first().distance == pointing["distance"]


@pytest.mark.django_db
def test_movement_station_axis_x(create_station, create_right_pointing_axis_x):
    station = create_station()
    start_position_x = station.position_x
    pointing = create_right_pointing_axis_x()
    assert start_position_x + pointing.distance == station.position_x


@pytest.mark.django_db
def test_movement_station_axis_y(create_station, create_right_pointing_axis_y):
    """
    Test creation of point with plus Y direction
    """
    station = create_station()
    start_position_y = station.position_y
    pointing = create_right_pointing_axis_y()
    assert start_position_y + pointing.distance == station.position_y


@pytest.mark.django_db
def test_movement_station_axis_z(create_station, create_right_pointing_axis_z):
    station = create_station()
    start_position_z = station.position_z
    pointing = create_right_pointing_axis_z()
    assert start_position_z + pointing.distance == station.position_z


@pytest.mark.django_db
def test_station_condition_before_pointing(create_station):
    station = create_station()
    assert station.condition == "running"


@pytest.mark.django_db
def test_station_condition_after_right_pointing_axis_x(create_station, create_right_pointing_axis_x):
    station = create_station()
    pointing = create_right_pointing_axis_x()
    assert station.condition == "running"


@pytest.mark.django_db
def test_station_condition_after_left_pointing_axis_x(create_station, create_left_pointing_axis_x):
    station = create_station()
    pointing = create_left_pointing_axis_x()
    assert station.condition == "broken"
