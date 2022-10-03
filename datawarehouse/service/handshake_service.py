import sqlalchemy


# How to use HandshakeService:
# 1. Create a new HandshakeService object with the database url.
#   (a) The engine will be initialized.
#   (b) The connection will be initialized.
#   (c) The metadata will be initialized.
#   (d) The tables will be created, but not added.
# 2. Call the insert_tables() method to insert the newly-created tables.
# 3. Call the insert_data(json) method to insert the data.
# 4. Call the close_connection() method to close the connection.
# NOTE: Right now this only supports one group.
class HandshakeService:
    def __init__(self, url):
        # Database connection variables.
        self.__engine = sqlalchemy.create_engine(url)
        self.__connection = self.__engine.connect()

        # Table variables.
        self.__metadata_obj = sqlalchemy.MetaData()
        self.__group_table = self.__build_group_table()
        self.__source_table = self.__build_source_table()
        self.__metric_table = self.__build_metric_table()

    # Insert the tables into the database.
    def insert_tables(self):
        self.__group_table.create(self.__engine)
        self.__source_table.create(self.__engine)
        self.__metric_table.create(self.__engine)

    # Close the connection to the database.
    def close_connection(self):
        self.__connection.close()

    # Give this method `data` (JSON file) and it will insert the data into the database.
    def insert_data(self, data):
        group_insert = self.__group_table.insert().values(
            name=data["group_name"], classification=data["classification"]
        )
        self.__connection.execute(group_insert)

        # suid will keep track of the source_uid for the source table.
        # When we move on to the next source, we will increment suid.
        suid = 1
        for source in data["sources"]:
            source_insert = self.__source_table.insert().values(
                group_uid=1, name=source["name"]
            )
            self.__connection.execute(source_insert)
            for metric in source["metrics"]:
                metric_insert = self.__metric_table.insert().values(
                    source_uid=suid,
                    name=metric["name"],
                    units=metric["units"],
                    data_type=metric["data_type"],
                    asc=metric["asc"],
                )
                self.__connection.execute(metric_insert)
            suid += 1

    # Private function. Builds the group table.
    # Visualization of the group table:
    # group_uid | name | location | classification
    # --------------------------------------------
    def __build_group_table(self):
        group_table = sqlalchemy.Table(
            "group",
            self.__metadata_obj,
            sqlalchemy.Column(
                "group_uid", sqlalchemy.Integer, primary_key=True, autoincrement=True
            ),
            sqlalchemy.Column("name", sqlalchemy.String),
            sqlalchemy.Column("location", sqlalchemy.String),
            sqlalchemy.Column("classification", sqlalchemy.String),
        )
        return group_table

    # Private function. Builds the source table.
    # Visualization of the source table:
    # source_uid | group_uid | name | tz_info
    # ----------------------------------------
    def __build_source_table(self):
        source_table = sqlalchemy.Table(
            "source",
            self.__metadata_obj,
            sqlalchemy.Column(
                "source_uid", sqlalchemy.Integer, primary_key=True, autoincrement=True
            ),
            sqlalchemy.Column(
                "group_uid",
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(self.__group_table.c.group_uid),
            ),
            sqlalchemy.Column("name", sqlalchemy.String),
            sqlalchemy.Column("tz_info", sqlalchemy.String),
        )
        return source_table

    # Private function. Builds the metric table.
    # Visualization of the metric table:
    # metric_uid | source_uid | data_type | units | name | asc
    # --------------------------------------------------------
    def __build_metric_table(self):
        metric_table = sqlalchemy.Table(
            "metric",
            self.__metadata_obj,
            sqlalchemy.Column(
                "metric_uid", sqlalchemy.Integer, autoincrement=True, primary_key=True
            ),
            sqlalchemy.Column(
                "source_uid",
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(self.__source_table.c.source_uid),
            ),
            sqlalchemy.Column("data_type", sqlalchemy.String),
            sqlalchemy.Column("units", sqlalchemy.String),
            sqlalchemy.Column("name", sqlalchemy.String),
            sqlalchemy.Column("asc", sqlalchemy.Boolean),
        )
        return metric_table
