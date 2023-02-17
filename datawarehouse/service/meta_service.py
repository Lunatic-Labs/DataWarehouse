from datawarehouse.model import group, source, metric
from datawarehouse.config.db import config as db
from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import UUID
from datawarehouse.service import BaseService

parents = dict(source="group", metric="source")


class MetaService(BaseService):
    session = db.session

    def getNameFromUID(self, level, uid):
        table = self._get_table(level)
        with self.session() as s:
            ret = (
                s.query(table.c.name)
                .where(getattr(table.c, level + "_uid") == uid)
                .scalar()
            )
        return ret

    # this function breaks on the query line. Not sure why. must investigate.
    def ensureGroupOwnershipOfSource(self, group_uid, source_uid):
        table = self._get_table("source")
        with self.session() as s:
            row = (
                s.query(table)
                .where(
                    and_(
                        table.c.group_uid == group_uid,
                        table.c.source_uid == source_uid,
                    )
                )
                .first()
            )
        return row is not None
        # return True

    def getSourcesFromGroup(self, group_uid):
        table = self._get_table("source")
        with self.session() as s:
            rows = s.query(table).where(table.c.group_uid == group_uid).all()
        return rows

    def getMetricsFromSource(self, source_uid):
        table = self._get_table("metric")
        with self.session() as s:
            rows = s.query(table).where(table.c.source_uid == source_uid).all()
        return rows

    def getGroupInfo(self, group_uid) -> dict:
        table = self._get_table("group")
        with self.session() as s:
            row = s.query(table).where(table.c.group_uid == group_uid).first()
        return row._asdict()

    def getMetadata(self, uids: dict) -> dict:
        if "group_uid" not in uids.keys():
            raise Exception("missing group_uid")

        group_uid = uids["group_uid"]
        resp_dict = dict(**self.getGroupInfo(group_uid))
        resp_dict.update(**dict(sources=[]))

        for row in self.getSourcesFromGroup(group_uid):
            # if there are sources requested, only return those sources
            if "sources" in uids.keys():
                if row.source_uid not in uids["sources"]:
                    continue

            source_uid = row.source_uid
            metrics = self.getMetricsFromSource(source_uid)
            source_dict = row._asdict()
            # if there are metrics requested, only return those metrics
            source_dict.update(**dict(metrics=[]))
            for mtrc in metrics:
                if "metrics" in uids.keys():
                    if mtrc.metric_uid not in uids["metrics"]:
                        continue
                source_dict["metrics"].append(mtrc._asdict())

            resp_dict["sources"].append(source_dict)

        return resp_dict
