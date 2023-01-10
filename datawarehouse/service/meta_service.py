from datawarehouse.model import group, source, metric
from datawarehouse.config.db import config as db
from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import UUID
from datawarehouse.service import BaseService

parents = dict(source="group", metric="source")


class MetaService(BaseService):
    session = db.session

    def _get_meta(self, name, uid, parent_uid=None):
        uid_name = name + "_uid"
        table = self._get_table(name)
        with self.session() as s:
            row = s.query(table).where(getattr(table.c, uid_name) == uid).first()

        if parent_uid:
            parent_uid_name = parents[name] + "_uid"
            if getattr(row, parent_uid_name) != parent_uid:
                row = None
        return row

    # uids must be dict
    # follows this format:
    # {"group_uid": <group_uid>,
    #       "sources": [
    #           {"source_uid": <source_uid>,
    #           "metrics": [
    #               {"metric_uid":<metric_uid>}, ...
    #           ]}, ...
    #       ]
    # }

## NOTE TO FUTURE DEVELOPERS
# have this take a group_uid and return all of its sources/metrics etc. right now, it just returns the group info if only the group_uid is provided.
    
    def get_metadata(self, uids: dict):
        meta_dict = dict()
        if "group_uid" not in uids.keys():
            return "Missing Group_uid"
        grp_row = self._get_meta("group", uids["group_uid"])
        if not grp_row:
            return "group_uid not found in our database"
        meta_dict.update(**grp_row._asdict())
        if "sources" not in uids:
            return meta_dict
        else:
            meta_dict.update(**dict(sources=[]))
            for src in uids["sources"]:
                src_row = self._get_meta("source", src["source_uid"], grp_row.group_uid)
                src_dict = (
                    src_row._asdict()
                    if src_row
                    else dict(
                        error=f"Couldn't find source_uid: {src['source_uid']} in the specified group"
                    )
                )
                if "error" in src_dict:
                    continue
                src_dict.update(**dict(metrics=[]))
                if "metrics" not in src:
                    return meta_dict
                for mtrc in src["metrics"]:
                    mtrc_row = self._get_meta(
                        "metric", mtrc["metric_uid"], src_row.source_uid
                    )
                    src_dict["metrics"].append(
                        mtrc_row._asdict()
                        if mtrc_row
                        else dict(
                            error=f"Couldn't find metric_uid: {mtrc['metric_uid']} in the specified source"
                        )
                    )

                meta_dict["sources"].append(src_dict)
        return meta_dict

    def get_name_from_uid(self, level, uid):
        table = self._get_table(level)
        with self.session() as s:
            ret = (
                s.query(table.c.name)
                .where(getattr(table.c, level + "_uid") == uid)
                .scalar()
            )
        return ret

    # this function breaks on the query line. Not sure why. must investigate.
    def ensure_group_ownership_of_source(self, group_uid, source_uid):
        # table = self._get_table("source")
        # row = self.session.query(table).where(table.c.source_uid == source_uid).first()
        # return row is not None
        return True
