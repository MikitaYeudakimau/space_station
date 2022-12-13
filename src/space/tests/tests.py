import pytest

from space import models


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
    station_data, pointing_data = create_right_pointing_axis_x
    assert models.Pointing.objects.count() == 1
    assert models.Pointing.objects.first().axis == pointing_data["axis"]
    assert models.Pointing.objects.first().distance == pointing_data["distance"]


@pytest.mark.django_db
def test_right_pointing_axis_y(create_right_pointing_axis_y):
    """
    Test creation of point with positive Y direction
    """
    station_data, pointing_data = create_right_pointing_axis_y
    assert models.Pointing.objects.count() == 1
    assert models.Pointing.objects.first().axis == pointing_data["axis"]
    assert models.Pointing.objects.first().distance == pointing_data["distance"]


@pytest.mark.django_db
def test_right_pointing_axis_z(create_right_pointing_axis_z):
    """
    Test creation of point with positive Z direction
    """
    station_data, pointing_data = create_right_pointing_axis_z
    assert models.Pointing.objects.count() == 1
    assert models.Pointing.objects.first().axis == pointing_data["axis"]
    assert models.Pointing.objects.first().distance == pointing_data["distance"]


@pytest.mark.django_db
def test_movement_station_axis_x(create_right_pointing_axis_x):
    """
    Test change of station X-coordinate
    """
    station_data, pointing_data = create_right_pointing_axis_x
    start_position_x = station_data['position_x']
    pointing = pointing_data['distance']
    end_position_x = models.SpaceStation.objects.get(pk=station_data['id']).position_x
    assert start_position_x + pointing == end_position_x


@pytest.mark.django_db
def test_movement_station_axis_y(create_right_pointing_axis_y):
    """
    Test change of station Y-coordinate
    """
    station_data, pointing_data = create_right_pointing_axis_y
    start_position_y = station_data['position_y']
    pointing = pointing_data['distance']
    end_position_y = models.SpaceStation.objects.get(pk=station_data['id']).position_y
    assert start_position_y + pointing == end_position_y


@pytest.mark.django_db
def test_movement_station_axis_z(create_right_pointing_axis_z):
    """
    Test change of station Z-coordinate
    """
    station_data, pointing_data = create_right_pointing_axis_z
    start_position_z = station_data['position_z']
    pointing = pointing_data['distance']
    end_position_z = models.SpaceStation.objects.get(pk=station_data['id']).position_z
    assert start_position_z + pointing == end_position_z


@pytest.mark.django_db
def test_station_condition_before_pointing(create_station):
    """
    Check station status after creation
    """
    station_condition = create_station['condition']
    assert station_condition == "running"


@pytest.mark.django_db
def test_station_condition_after_right_pointing_axis_x(create_right_pointing_axis_x):
    """
    Check station status after positive X movement
    """
    station_data, pointing_data = create_right_pointing_axis_x
    station = models.SpaceStation.objects.get(pk=station_data['id'])
    assert station.condition == "running"


@pytest.mark.django_db
def test_station_condition_after_left_pointing_axis_x(create_left_pointing_axis_x):
    """
    Check station status after negative X movement
    """
    station_data, pointing_data = create_left_pointing_axis_x
    station = models.SpaceStation.objects.get(pk=station_data['id'])
    assert station.condition == "broken"


@pytest.mark.django_db
def test_station_condition_after_left_pointing_axis_y(create_left_pointing_axis_y):
    """
    Check station status after negative Y movement
    """
    station_data, pointing_data = create_left_pointing_axis_y
    station = models.SpaceStation.objects.get(pk=station_data['id'])
    assert station.condition == "broken"


@pytest.mark.django_db
def test_station_condition_after_left_pointing_axis_z(create_left_pointing_axis_z):
    """
    Check station status after negative Z movement
    """
    station_data, pointing_data = create_left_pointing_axis_z
    station = models.SpaceStation.objects.get(pk=station_data['id'])
    assert station.condition == "broken"
