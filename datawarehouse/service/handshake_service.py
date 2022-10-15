"""
This service handles the logic to take in a new group/source and store the data given by the client in the metadata tables
"""
import sqlalchemy
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
    _engine = db.engine
    _metadata_obj = db.meta

    @property
    def _connection(self):
        return self._engine.connect()

    """
    prepareTables(self, properties) -> dict 
    Public method. Takes properties: JSON and does the following:
        1. inserts the metadata into the meta tables (group, source, metric)
        2. kicks off the generation of the described tables 
    """

    @classmethod
    def prepareTables(self, properties):
        uids = self._insertMetadata(properties)
        # the creating of the tables will go here.
        self._createTables(uids)
        return uids

    """
    _insertMetadata(self, json_properties) -> dict.
    Private method. Takes data: JSON, and does the following:
        1. begins the chain of methods that insert the metadata
            a. calls _addGroup()
    """

    @classmethod
    def _insertMetadata(self, json_properties):
        # NOTE: Eventually we will add the feature to add a source/metric to an existing group... Will have to rework this later.
        uids = self._addGroup(**json_properties)
        return uids

    """
    _addGroup(self, group_name, location, classification, sources) -> dict
    Private Method. Takes group_name: string, location: optional string, classification: optional string, and sources: required array of dicts
    Does the following :
        1. generates a unique uuid identifier 
        2. commits the group data to the group table in the database
        3. begins insertion of source data by calling _addSources()
        4. returns the gathered data
    """

    @classmethod
    def _addGroup(self, group_name, location=None, classification=None, sources=[]):
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
        sources = self._addSources(group_uid, sources)

        group_properties.update(dict(sources=sources, group_uid=group_uid))
        return group_properties

    """
    _addSource(self, group_uid, sources) -> dict
    Private Method. Takes group_uid: uuid4, sources: required array of dicts
    Does the following :
        1. generates a unique uuid identifier for the source and adds it to the json data 
        2. commits the source data to the source table in the database
        3. begins insertion of metric data by calling _addMetrics()
        4. returns the gathered data
    """

    @classmethod
    def _addSources(self, group_uid, sources):
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
            metrics = self._addMetrics(source_uid, s["metrics"])

            # add updated metrics to dict, add source_uid
            s.update(dict(metrics=metrics, source_uid=source_uid))
            source_uids.append(s)
        return source_uids

    """
    _addMetrics(self, source_uid, metrics) -> dict
    Private Method. Takes source_uid: uuid4, metrics: required array of dicts
    Does the following :
        1. generates a unique uuid identifier for the metric and adds it to the json data 
        2. commits the metric data to the metric table in the database
        3. returns the gathered data
    """

    @classmethod
    def _addMetrics(self, source_uid, metrics):
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

    """
    createTables(self, data) -> void.
    Public method. Takes data: JSON, and does the following:
        1. Create tables based off of the `source` name and append
           a unique number.
        2. Append the source's `name` of source's type `data_type`
           with a unique MUID.
        3. Appends a timestamp column.
        4. Add the table to the data_warehouse database.
    """

    @classmethod
    def _createTables(self, data):
        # Used for keeping track of the table number and a unique name.
        table_num = 0

        # Navigate through `sources` part of the dictionary.
        for src in data["sources"]:
            table = sqlalchemy.Table(src["source_uid"], self._metadata_obj)

            # Append new columns in `table` with the name, `name`, and the data type, `data_type`.
            muid = 1
            for metric in src["metrics"]:
                col_name = metric["metric_uid"]
                col_type = self._getType(metric["data_type"])
                table.append_column(sqlalchemy.Column(col_name, col_type))
                muid += 1
            table.append_column(sqlalchemy.Column("timestamp", sqlalchemy.DateTime))

            # Insert the table into the database.
            table.create(self._engine)
            table_num += 1

    """
    _getType(self, type) -> sqlalchemy.Type.
    Private method. Takes type: String, and determines the
    appropriate sqlalchemy.Type to return.
    """

    @classmethod
    def _getType(self, type_):
        # Horrible code, but this will be refactored later.
        # This is just for testing for now. I am leaving the
        # string comparisons also for testing purposes.
        if type_ == "integer" or (type(type_) == type(0) and type_ == 1):
            return sqlalchemy.Integer
        elif type_ == "float" or (type(type_) == type(0.0) and type_ == 2):
            return sqlalchemy.Float
        elif type_ == "bool" or (type(type_) == type(False) and type_ == 3):
            return sqlalchemy.Boolean
        elif type_ == "string" or (type(type_) == type("data") and type_ == 4):
            return sqlalchemy.String
        assert False, "HandshakeService ERROR: INVALID TYPE. {}".format(type_)

    """
    closeConnection(self) -> void.
    Public method. Closes the database connection.
    """

    def closeConnection(self):
        self._connection.close()
