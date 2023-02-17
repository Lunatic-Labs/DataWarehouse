import pytest

from sqlalchemy import delete, insert
from uuid import uuid4 as uuid4_


@pytest.fixture(scope="module")
def populate_meta_tables():
    from datawarehouse.model import metric, source, group
    from datawarehouse.config.db import config as db

    def uuid4():
        return str(uuid4_())

    # populate tables
    source_uids = []
    metric_uids = []
    with db.session() as s:
        s.begin()
        group_uid = uuid4()
        s.execute(insert(group).values(group_uid=group_uid, name="test_group"))
        for i in range(3):
            source_uid = uuid4()
            s.execute(
                insert(source).values(
                    source_uid=source_uid, name=f"test_source{i}", group_uid=group_uid
                )
            )
            metric_uid = uuid4()
            s.execute(
                insert(metric).values(
                    metric_uid=metric_uid,
                    name=f"test_metric{i}",
                    source_uid=source_uid,
                    data_type=f"{i}",
                    units=f"test_units{i}",
                )
            )
            source_uids.append(source_uid)
            metric_uids.append(metric_uid)

        s.commit()

    yield group_uid, source_uids, metric_uids

    # cleanup
    with db.session() as s:
        s.begin()
        for source_uid in source_uids:
            s.execute(delete(metric).where(metric.c.source_uid == source_uid))
        s.execute(delete(source).where(source.c.group_uid == group_uid))
        s.execute(delete(group).where(group.c.group_uid == group_uid))
        s.commit()


def test_getNameFromUID(populate_meta_tables):
    from datawarehouse.service.meta_service import MetaService

    group_uid, *_ = populate_meta_tables
    service = MetaService()
    assert service.getNameFromUID("group", group_uid) == "test_group"


@pytest.mark.xfail
def test_xfail_getNameFromUID(populate_meta_tables):
    from datawarehouse.service.meta_service import MetaService

    service = MetaService()

    assert service.getNameFromUID("group", str(uuid4_())) == "test_group"


def test_ensureGroupOwnershipOfSource(populate_meta_tables):
    from datawarehouse.service.meta_service import MetaService

    group_uid, source_uids, metric_uids = populate_meta_tables
    service = MetaService()
    for source_uid in source_uids:
        assert service.ensureGroupOwnershipOfSource(group_uid, source_uid)


@pytest.mark.xfail
def test_xfail_ensureGroupOwnershipOfSource(populate_meta_tables):
    from datawarehouse.service.meta_service import MetaService

    group_uid, source_uids, metric_uids = populate_meta_tables
    service = MetaService()
    assert service.ensureGroupOwnershipOfSource(group_uid, str(uuid4_()))


def test_getSourcesFromGroup(populate_meta_tables):
    from datawarehouse.service.meta_service import MetaService

    group_uid, source_uids, metric_uids = populate_meta_tables
    service = MetaService()
    sources = service.getSourcesFromGroup(group_uid)
    assert len(sources) == 3
    for source_uid in source_uids:
        assert source_uid in [source.source_uid for source in sources]


def test_getMetricsFromSource(populate_meta_tables):
    from datawarehouse.service.meta_service import MetaService

    group_uid, source_uids, metric_uids = populate_meta_tables
    service = MetaService()
    for source_uid in source_uids:

        metrics = service.getMetricsFromSource(source_uid)
        assert len(metrics) == 1
        assert metrics[0].metric_uid in metric_uids


def test_getGroupInfo(populate_meta_tables):
    from datawarehouse.service.meta_service import MetaService

    group_uid, source_uids, metric_uids = populate_meta_tables
    service = MetaService()
    group_info = service.getGroupInfo(group_uid)
    assert group_info.get("name", None) == "test_group"
    assert group_info.get("group_uid", None) == group_uid


def test_getMetadata(populate_meta_tables):
    from datawarehouse.service.meta_service import MetaService

    group_uid, source_uids, metric_uids = populate_meta_tables
    service = MetaService()
    payload = dict(group_uid=group_uid, sources=source_uids, metrics=metric_uids)
    metadata = service.getMetadata(payload)

    assert metadata.get("group_uid", None) == group_uid
    assert metadata.get("name", None) == "test_group"
    sources = metadata.get("sources", None)
    assert len(sources) == 3
    for source_uid in source_uids:
        assert source_uid in [source.get("source_uid", None) for source in sources]

    for source in metadata.get("sources", []):
        metrics = source.get("metrics", [])
        assert len(metrics) == 1
        assert metrics[0].get("metric_uid", None) in metric_uids


def test_getMetadata_specific_source(populate_meta_tables):
    from datawarehouse.service.meta_service import MetaService

    group_uid, source_uids, metric_uids = populate_meta_tables
    service = MetaService()
    payload = dict(group_uid=group_uid, sources=[source_uids[0]], metrics=metric_uids)
    metadata = service.getMetadata(payload)

    assert metadata.get("group_uid", None) == group_uid
    assert metadata.get("name", None) == "test_group"
    sources = metadata.get("sources", None)
    assert len(sources) == 1
    assert source_uids[0] in [source.get("source_uid", None) for source in sources]

    for source in metadata.get("sources", []):
        metrics = source.get("metrics", [])
        assert len(metrics) == 1
        assert metrics[0].get("metric_uid", None) in metric_uids
