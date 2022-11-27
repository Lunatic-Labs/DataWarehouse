from . import test_app, session, engine
import pytest

from datawarehouse.service.query_service import op_to_sa_op


from sqlalchemy import insert, delete


@pytest.fixture(scope="session")
def create_and_seed_table(test_app, engine, session):
    session.begin()
    session.execute("drop table if exists \"4f256af2-fb4f-4920-89c7-3c839a213d21\"")
    session.execute(
        """
        CREATE TABLE public.\"4f256af2-fb4f-4920-89c7-3c839a213d21\" (
            \"9e498b97-a09d-44d0-ad47-54019ae87945\" int NULL,
            \"af5da2ef-7208-4ea9-b2f5-a39488e66930\" varchar NULL,
            \"dd999164-db5f-4e8e-9c47-9cb49ae3d294\" float8 NULL,
            \"timestamp\" timestamp NULL
        );
    """
    )
    session.execute("""
        DELETE FROM public.metric
        WHERE metric_uid='dd999164-db5f-4e8e-9c47-9cb49ae3d294'::uuid;
        DELETE FROM public.metric
        WHERE metric_uid='af5da2ef-7208-4ea9-b2f5-a39488e66930'::uuid;
        DELETE FROM public.metric
        WHERE metric_uid='9e498b97-a09d-44d0-ad47-54019ae87945'::uuid;
    """)
    session.execute("""
        DELETE FROM public."source"
        WHERE source_uid='4f256af2-fb4f-4920-89c7-3c839a213d21'::uuid;
    """)
    session.execute("""
        DELETE FROM public."group"
        WHERE group_uid='4f256af2-fb4f-4920-89c7-3c839a213d21'::uuid;
    """)
    session.commit()
    # from datawarehouse.service import BaseService
    # srvc = BaseService()
    # table = srvc._get_table("pytest_table")

    session.begin()
    session.execute(
        """INSERT INTO public.\"4f256af2-fb4f-4920-89c7-3c839a213d21\"
        (\"9e498b97-a09d-44d0-ad47-54019ae87945\", \"af5da2ef-7208-4ea9-b2f5-a39488e66930\", \"dd999164-db5f-4e8e-9c47-9cb49ae3d294\")
        VALUES(1, 'test_string', 1.0);
        INSERT INTO public.\"4f256af2-fb4f-4920-89c7-3c839a213d21\"
        (\"9e498b97-a09d-44d0-ad47-54019ae87945\", \"af5da2ef-7208-4ea9-b2f5-a39488e66930\", \"dd999164-db5f-4e8e-9c47-9cb49ae3d294\")
        VALUES(50, 'larger_string', 50.0);
        INSERT INTO public.\"4f256af2-fb4f-4920-89c7-3c839a213d21\"
        (\"9e498b97-a09d-44d0-ad47-54019ae87945\", \"af5da2ef-7208-4ea9-b2f5-a39488e66930\", \"dd999164-db5f-4e8e-9c47-9cb49ae3d294\")
        VALUES(10, 'different', -1.1);
    """
    )
    session.execute("""
        INSERT INTO public."group"
        ("name", "location", classification, group_uid)
        VALUES('pytest_group', NULL, NULL, '4f256af2-fb4f-4920-89c7-3c839a213d21'::uuid);
    """)
    session.execute("""
        INSERT INTO public."source"
        (source_uid, "name", group_uid, tz_info)
        VALUES('4f256af2-fb4f-4920-89c7-3c839a213d21'::uuid, 'pytest_source', '4f256af2-fb4f-4920-89c7-3c839a213d21'::uuid, NULL);
    """)
    session.execute("""
        INSERT INTO public.metric
        (metric_uid, source_uid, data_type, units, "name", "asc")
        VALUES('dd999164-db5f-4e8e-9c47-9cb49ae3d294'::uuid, '4f256af2-fb4f-4920-89c7-3c839a213d21'::uuid, 'float', NULL, 'float1', true);
        INSERT INTO public.metric
        (metric_uid, source_uid, data_type, units, "name", "asc")
        VALUES('af5da2ef-7208-4ea9-b2f5-a39488e66930'::uuid, '4f256af2-fb4f-4920-89c7-3c839a213d21'::uuid, 'string', NULL, 'string1', true);
        INSERT INTO public.metric
        (metric_uid, source_uid, data_type, units, "name", "asc")
        VALUES('9e498b97-a09d-44d0-ad47-54019ae87945'::uuid, '4f256af2-fb4f-4920-89c7-3c839a213d21'::uuid, 'integer', NULL, 'integer1', true);
    """)
    session.commit()

class Col_op_val:
    def __init__(self, col, op, val):
        self.col = col
        self.op = op 
        self.val = val


def create_query_string(*col_op_vals):
    criteria = []
    for c in col_op_vals:
        criteria.append(f"{c.col}__{c.op}={str(c.val)}")
    return "?"+"&".join(criteria)

@pytest.mark.parametrize(
    "column, op, val, rows_expected",
    [
        ("integer1", "eq", 1, 1),
        ("integer1", "<", 49, 2),
        ("integer1", "<<", 50, 3),
        ("string1", "like", "%stri%", 2),
        ("string1", "contains", "string", 2),
        ("float1", ">>", 1.0, 2),
    ],
)
def test_query(
    test_app,
    session,
    create_and_seed_table,
    column, op, val, rows_expected
):
    qs = create_query_string(Col_op_val(column, op, val))

    resp = test_app.get("api/query/4f256af2-fb4f-4920-89c7-3c839a213d21/4f256af2-fb4f-4920-89c7-3c839a213d21/" + qs)
    
    assert resp.status_code == 200
    json = resp.json

    assert len(json.keys()) == rows_expected