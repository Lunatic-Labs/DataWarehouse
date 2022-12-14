import json
import pytest
from . import test_app
from faker import Faker
from uuid import uuid4


def pytest_configure():
    pytest.cleanup_uids = dict(group=[], source=[], metric=[])


@pytest.fixture(scope="function")
def handshake_json():
    fake = Faker()
    unique_group_name = str(uuid4())
    pytest.cleanup_uids["group"].append(unique_group_name)
    json = {
        "group_name": unique_group_name,
        "classification": "testing",
        "sources": [],
        "location": fake.pystr(),
    }
    for i in range(fake.pyint(min_value=1, max_value=10)):
        json["sources"].append(generate_source())
    return json


def generate_source():
    fake = Faker()
    source_name = str(uuid4())
    pytest.cleanup_uids["source"].append(source_name)
    dic = {
        "name": source_name,
        "metrics": [],
        "tz_info": fake.pystr(),
    }
    for i in range(fake.pyint(min_value=1, max_value=10)):
        dic["metrics"].append(generate_metric())

    return dic


def generate_metric():
    fake = Faker()
    metric_name = str(uuid4())
    pytest.cleanup_uids["metric"].append(metric_name)
    return {
        "name": metric_name,
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


@pytest.fixture(scope="session")
def session():
    pytest_configure()
    from datawarehouse.config.db import config
    from datawarehouse.util import get_table, drop_table
    from sqlalchemy import delete
    from sqlalchemy.orm import Session

    yield config.session

    from datawarehouse import model

    with Session(config.engine) as s:
        s.begin()
        for layer in ["metric", "source", "group"]:
            table = getattr(model, layer)
            if layer == "source":
                for uid in pytest.cleanup_uids[layer]:
                    source_uid = (
                        s.query(table.c.source_uid).where(table.c.name == uid).scalar()
                    )
                    drop_table(source_uid)
            stmt = delete(table).where(table.c.name.in_(pytest.cleanup_uids[layer]))
            s.execute(stmt)
        s.commit()


def check_required_fields(required_fields, db_row, checked_object):
    for required_field in required_fields:
        db_column = getattr(db_row, required_field)
        assert db_column and db_column == checked_object[required_field]


def check_optional_fields(optional_fields, db_row, checked_object):
    valid = True
    for optional_field in optional_fields:
        db_column = getattr(db_row, optional_field)
        if db_column and optional_field in checked_object:
            assert db_column == checked_object[optional_field]


required_fields = {
    "group": ["name", "group_uid"],
    "source": ["name", "source_uid"],
    "metric": ["metric_uid", "name", "data_type"],
}
optional_fields = {
    "group": ["classification", "location"],
    "source": ["tz_info"],
    "metric": ["units", "asc"],
}


def parametrize_missing_fields(fields):
    return_val = []
    for item in [x for x in fields["group"] if "uid" not in x]:
        tup = ([], item)
        return_val.append(tup)

    for item in [x for x in fields["source"] if "uid" not in x]:
        tup = (["sources", 0], item)
        return_val.append(tup)

    for item in [x for x in fields["metric"] if "uid" not in x]:
        tup = (["sources", 0, "metrics", 0], item)
        return_val.append(tup)

    return return_val


def check_handshake_response(response, session):
    assert response.status_code == 200
    from datawarehouse.model import group, source, metric

    resp_json = response.json
    group_uid = resp_json["group_uid"]
    group_row = session.query(group).where(group.c.group_uid == group_uid).first()
    check_required_fields(required_fields["group"], group_row, resp_json)
    check_optional_fields(optional_fields["group"], group_row, resp_json)

    for src in resp_json["sources"]:
        src_uid = src["source_uid"]
        src_row = session.query(source).where(source.c.source_uid == src_uid).first()
        check_required_fields(required_fields["source"], src_row, src)
        check_optional_fields(optional_fields["source"], src_row, src)

        for mtrc in src["metrics"]:
            metric_uid = mtrc["metric_uid"]
            metric_row = (
                session.query(metric).where(metric.c.metric_uid == metric_uid).first()
            )

            check_required_fields(required_fields["metric"], metric_row, mtrc)
            check_optional_fields(optional_fields["metric"], metric_row, mtrc)


def test_handshake(test_app, handshake_json, session):
    response = test_app.post("/api/prepare/", json=handshake_json)
    assert response.status_code == 200
    check_handshake_response(response, session)


@pytest.mark.parametrize(
    "layer, missing_field", parametrize_missing_fields(required_fields)
)
def test_missing_required_fields(
    test_app, session, handshake_json, layer, missing_field
):
    json_payload = handshake_json
    for l in layer:
        json_payload = json_payload[l]

    # this will be removed. We need to rename the handshake attribute "group_name" to just "name"
    if layer == [] and missing_field == "name":
        missing_field = "group_name"

    del json_payload[missing_field]

    response = test_app.post("/api/prepare/", json=handshake_json)
    assert (
        response.status_code == 500
    )  # This will change later once jerry finishes the checker funciton


@pytest.mark.parametrize(
    "layer, missing_field", parametrize_missing_fields(optional_fields)
)
def test_missing_optional_fields(
    test_app, session, handshake_json, layer, missing_field
):
    json_payload = handshake_json
    for l in layer:
        json_payload = json_payload[l]

    del json_payload[missing_field]

    response = test_app.post("/api/prepare/", json=handshake_json)

    check_handshake_response(response, session)
