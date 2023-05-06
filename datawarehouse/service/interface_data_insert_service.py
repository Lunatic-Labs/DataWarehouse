import sqlalchemy
import json
import ast

from datawarehouse.service import BaseService

from datetime import datetime
from datawarehouse.config.db import config as db

from datawarehouse.model import metric


class InterfaceInsertDataService(BaseService):
    session = db.session
    
    # Takes a string and imports it into a json formated file
    # Need to check and see how the string will be formated but works with a string formated like this:
    # Format of string passed to function "4aa950ae-f350-4a51-a21d-07817cd408e1`ac64dfb2-3d0f-48b5-88ab-cedf1a0c13d1`50"
    # Final string format: '{ "source_uid": "4aa950ae-f350-4a51-a21d-07817cd408e1", "metrics":[ {"metric_uid": "ac64dfb2-3d0f-48b5-88ab-cedf1a0c13d1", "value": "50"} ] }'
    def dataToJSON(self, data): #take in the interface data
        str = data.split('`')

        parsed_string = {'source_uid': str[0], 
                        'metric_uid': str[1], 
                        'value': int(str[2])}

        formatted_string = '{ "source_uid": "%(source_uid)s", "metrics":[ {"metric_uid": "%(metric_uid)s", "value": %(value)d} ] }' % parsed_string

        json_string = ast.literal_eval(formatted_string)
        json_object = json.loads(formatted_string)

        # json_object = json.dumps(json_string, indent=4)
        # with open("insert.out", "w") as outfile:
        #     outfile.write(json_object)

        return json_object #the created json

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
        print(type(data))
        table = self._get_table(data["source_uid"])
        values = {}
        for _metric in data["metrics"]:
            values[_metric["metric_uid"]] = _metric["value"]

        with self.session() as s:
            s.begin()
            stmt = table.insert().values({**values, "timestamp": datetime.now()})
            s.execute(stmt)
            s.commit()
