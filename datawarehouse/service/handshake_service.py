import sqlalchemy

from datawarehouse.service import BaseService

class HandshakeService(BaseService):
    def __init__(self, url):
        self._engine = sqlalchemy.create_engine(url)
        self._connection = self._engine.connect()
        self._metadata_obj = sqlalchemy.MetaData()

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

    def createTables(self, data):
        # Used for keeping track of the table number and a unique name.
        table_num = 0

        # Navigate through `sources` part of the dictionary.
        for source in data["sources"]:
            table = sqlalchemy.Table(
                "{}{}".format(source["name"], str(table_num)),
                self._metadata_obj,
            )

            # Append new columns in `table` with the name, `name`, and the data type, `data_type`.
            muid = 1
            for metric in source["metrics"]:
                col_name = "{} (MUID: {})".format(metric["name"], muid)
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

    def _getType(self, type):
        if type == "string":
            return sqlalchemy.String
        elif type == "integer":
            return sqlalchemy.Integer
        elif type == "float":
            return sqlalchemy.Float
        elif type == "bool":
            return sqlalchemy.Boolean
        assert False, "HandshakeService ERROR: INVALID TYPE. {}".format(type)

    """
    closeConnection(self) -> void.
    Public method. Closes the database connection.
    """

    def closeConnection(self):
        self._connection.close()
