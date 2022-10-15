import sqlalchemy
from datawarehouse.service import BaseService

from datetime import datetime
from datawarehouse.config.db import config as db

from datawarehouse.model import metric


class InsertDataService(BaseService):
    _engine = db.engine
    _connection = _engine.connect()
    _metadata_obj = db.meta

    # def __init__(self, url, source_uid=None, metric_uid=None, data=None):
    #     """
    #     TODO: Connect using our existing connections.
    #     """
    #     self._engine = db.engine
    #     self._connection = self._engine.connect()
    #     self._metadata_obj = db.meta

    """
    TODO: Change this from reading a txt file to taking JSON.
    """

    # def getData(self, file):
    #     with open(file, "r") as f:
    #         self._source_uid = f.readline()
    #         self._metric_uid = f.readline()
    #         self.data = f.readline()
    #         # Getting rid of the newline characters.
    #         self._source_uid = self._source_uid.rstrip()
    #         self._metric_uid = self._metric_uid.rstrip()
    #         self.data = self.data.rstrip()

    def _verifyInformation(self, data):

        for metric_ in data["metrics"]:
            stmt = sqlalchemy.select([metric]).where(
                metric.columns.metric_uid == metric_["metric_uid"]
            )
            result = self._connection.execute(stmt).fetchone()

            if result is None:
                raise Exception("metric_uid was not found.")

            if result["source_uid"] != data["source_uid"]:
                raise Exception(
                    "source_uid does not match the source_uid in the database."
                )

        print(f"Verified information for {result['name']}")

        # This is here if we want to do any type comparisons.
        # needed_type = self._connection.execute(
        #     sqlalchemy.select([metric_table.columns.data_type]).where(
        #         metric_table.c.metric_uid == self._metric_uid
        #     )
        # ).fetchone()[0]

    def addData(self, data):
        self._verifyInformation(data)

        # self._metadata_obj.reflect(self._engine)
        """
        NOTE: Found this function and may be useful.
        This is from the sqlalchemy inline documentation.

        Load all available table definitions from the database.
        Automatically creates ``Table`` entries in this ``MetaData`` for any
        table available in the database but not yet present in the
        ``MetaData``.  May be called multiple times to pick up tables recently
        added to the database, however no special action is taken if a table
        in this ``MetaData`` no longer exists in the database.
        """

        table = sqlalchemy.Table(
            data["source_uid"],
            self._metadata_obj,
            autoload=True,
            autoload_with=self._engine,
            keep_existing=True,
        )
        values = {}
        for _metric in data["metrics"]:
            values[_metric["metric_uid"]] = _metric["value"]
        stmt = table.insert().values({**values, "timestamp": datetime.now()})
        self._connection.execute(stmt)
