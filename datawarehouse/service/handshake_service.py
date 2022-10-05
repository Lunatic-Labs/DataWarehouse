import json
import sqlalchemy

# HandshakeService:
# 1. hss = HandshakeService(db_url).
#   (a) Engine will be initialized.
#   (b) Connection will be initialized.
#   (c) Metadata_obj will be initialized.
# 2. hss.create_and_insert_tables(json_data): Create the tables and insert the json data.
#   (a) __insert_data(): Inserts the actual data into the table.
# 3. hss.close_connection(): Close the connection.
class HandshakeService:
    def __init__(self, url):
        self.__engine = sqlalchemy.create_engine(url)
        self.__connection = self.__engine.connect()
        self.__metadata_obj = sqlalchemy.MetaData()

    def __insert_data(self, table, source):
        # Loop through the current `source`'s metrics to get actual values.
        for m in source["metrics"]:
            insert = table.insert().values(
                data_type=m["data_type"],
                units=m["units"],
                name=m["name"],
                asc=m["asc"],
            )
            self.__connection.execute(insert)

    def create_and_insert_tables(self, data):
        # Used for keeping track of the table number and a unique name.
        table_num = 0
        # Navigate through `sources` part of the dictionary.
        for source in data["sources"]:
            # Create a table based off of the current source.
            table = sqlalchemy.Table(
                source["name"] + str(table_num),  # Unique name.
                self.__metadata_obj,
                sqlalchemy.Column(
                    "metric_uid",
                    sqlalchemy.Integer,
                    primary_key=True,
                    autoincrement=True,
                ),
                sqlalchemy.Column("data_type", sqlalchemy.String),
                sqlalchemy.Column("units", sqlalchemy.String),
                sqlalchemy.Column("name", sqlalchemy.String),
                sqlalchemy.Column("asc", sqlalchemy.Boolean),
            )

            # Insert the table into the database.
            table.create(self.__engine)
            self.__insert_data(table, source)
            table_num += 1

    def close_connection(self):
        self.__connection.close()

    def write_json(self, data):
        with open("data.json", "w") as f:
            json.dump(data, f)
