"""
This service handles the logic to take in a new group/source and store the data given by the client in the metadata tables
"""

from datawarehouse.config.db import config as db
from datawarehouse.model import group, source, metric
from datawarehouse.service import BaseService

from sqlalchemy import func, insert
from uuid import uuid4 as _uuid4

# this is just to avoid repetative use of str() func on all the uuids...
def uuid4():
    return str(_uuid4())


class HandshakeService(BaseService):
    session = db.session

    """
    This function first calles _insert_metadata class method, which inserts the json data into the tables. 
    Then it calls the function to create all the tables that the client has specified. 
    """

    @classmethod
    def prepare_tables(self, properties):
        uids = self._insert_metadata(properties)
        # the creating of the tables will go here.
        return uids

    @classmethod
    def _insert_metadata(self, json_properties):
        # NOTE: Eventually we will add the feature to add a source/metric to an existing group... Will have to rework this later.
        uids = self._add_group(**json_properties)
        return uids

    @classmethod
    def _add_group(self, group_name, location=None, classification=None, sources=[]):
        group_uid = uuid4()
        group_properties = {
            "name": group_name,
            "location": location,
            "classification": classification,
            "group_uid": group_uid,
        }

        # The double asterisk is a way to unpack a dictionary. read more here https://medium.com/swlh/how-to-pack-and-unpack-data-in-python-tuples-and-dictionaries-55d218c65674
        # commit data to db
        stmt = insert(group).values(**group_properties)
        self.session.begin()
        self.session.execute(stmt)
        self.session.commit()

        # add source to db
        sources = self._add_sources(group_uid, sources)

        group_properties.update(dict(sources=sources, group_uid=group_uid))
        return group_properties

    @classmethod
    def _add_sources(self, group_uid, sources):
        source_uids = []
        for s in sources:
            source_uid = uuid4()
            source_props = {
                "source_uid": source_uid,
                "group_uid": group_uid,
                "name": s["name"],
            }

            # commit data to db
            stmt = insert(source).values(**source_props)
            self.session.begin()
            self.session.execute(stmt)
            self.session.commit()

            # add metrics to db
            metrics = self._add_metrics(source_uid, s["metrics"])

            # add updated metrics to dict, add source_uid
            s.update(dict(metrics=metrics, source_uid=source_uid))
            source_uids.append(s)
        return source_uids

    @classmethod
    def _add_metrics(self, source_uid, metrics):
        metric_uids = []
        for m in metrics:
            metric_uid = uuid4()

            # commit data to db
            stmt = insert(metric).values(
                source_uid=source_uid, metric_uid=metric_uid, **m
            )
            self.session.begin()
            self.session.execute(stmt)
            self.session.commit()

            # add metric_uid to dict
            m.update(dict(metric_uid=metric_uid))
            metric_uids.append(m)
        return metric_uids
