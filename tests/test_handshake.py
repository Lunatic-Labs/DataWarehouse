import pytest
from . import test_app
from faker import Faker


@pytest.fixture
def handshake_json():
    fake = Faker()
    json = {
        "group_name": fake.company(),
        "classification": "testing",
        "sources": [],
    }
    for i in range(fake.pyint(min_value=1, max_value=10)):
        json["sources"].append(generate_source())
    return json


def generate_source():
    fake = Faker()
    dic = {
        "name": fake.random_choices(
            elements=("thermometer", "Spedometer", "barometer"), length=1
        )[0],
        "metrics": [],
    }
    for i in range(fake.pyint(min_value=1, max_value=10)):
        dic["metrics"].append(generate_metric())

    return dic


def generate_metric():
    fake = Faker()
    return {
        "name": fake.pyint(),
        "units": fake.random_choices(
            elements=(
                "feet",
                "inches",
                "meters",
                "celcius",
                "kelvin",
                "students",
                "people",
                "vibrations",
            ),
            length=1,
        )[0],
        "data_type": fake.random_choices(
            elements=("integer", "float", "string"), length=1
        )[0],
        "asc": fake.pybool(),
    }


def test_handshake(test_app, handshake_json):
    response = test_app.post("/api/prepare/", json=handshake_json)
    assert response.status_code == 200
