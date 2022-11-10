import sqlalchemy
from datawarehouse.service import BaseService

from datetime import datetime
from datawarehouse.config.db import config as db

from datawarehouse.model import metric


class InsertDataService(BaseService):
    def verifyInformation(self, data):
        """
        verifyInformation(self, data) -> Err
        Verifies that the provided UUID's exist in the tables
        and verifies that they match.
        TODO: Type checking.
        """
        if not self._checkUUIDFormat(data["source_uid"]):
            return "source_uid is not a valid uuid4", 400
        for metric_ in data["metrics"]:
            if not self._checkUUIDFormat(metric_["metric_uid"]):
                return "metric_uid is not a valid uuid4", 400
            stmt = sqlalchemy.select([metric]).where(
                metric.c.metric_uid == metric_["metric_uid"]
            )
            result = self._connection.execute(stmt).first()
            if result is None:
                return "metric_uid was not found.", 400

            if result["source_uid"] != data["source_uid"]:
                return "source_uid does not match the source_uid in the database.", 400

        print(f"Verified information for {result['name']}")

        # This is here if we want to do any type comparisons.
        # needed_type = self._connection.execute(
        #     sqlalchemy.select([metric_table.columns.data_type]).where(
        #         metric_table.c.metric_uid == self._metric_uid
        #     )
        # ).fetchone()[0]

    def addData(self, data):
        """
        addData(self, data) -> void.
        Takes `data` JSON, parses and adds the value to the table.
        """
        table = self._get_table(data["source_uid"])
        values = {}
        for _metric in data["metrics"]:
            values[_metric["metric_uid"]] = _metric["value"]
        stmt = table.insert().values({**values, "timestamp": datetime.now()})
        self._connection.execute(stmt)
