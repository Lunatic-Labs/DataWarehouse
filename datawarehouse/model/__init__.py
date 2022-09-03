"""

    Currently we will be generating the models directly 
    from the database, instead of explicitly declaring models.
    This will allow us to add models on the fly without writing
    more code every time because they will be generated on startup.

"""


from sqlalchemy import Table
from sqlalchemy.ext.declarative import declared_attr
from datawarehouse.config import db
from sqlalchemy.ext.automap import automap_base
import sys

# __THIS__ is a list of modules available from this package.
__THIS__ = sys.modules[__name__]

# a mixin object that will allow us to add methods to all models we generate
class utilsMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


# Looks at the specified schema in the database defined by the Env var
# gets the metadata for the DB, and creates SqlAlchemy table objects with the info
def create_declaratives_for_schema(schema):
    metadata = db.config.meta
    engine = db.config.engine

    metadata.reflect(engine, views=True)

    # THIS ONly will work as long as we have tables with exactly one primary key... Will reassess if necessary.

    base = automap_base(metadata=metadata, cls=utilsMixin)
    base.prepare()
    return base.classes


declarative_objects = create_declaratives_for_schema("public")

tables = {do.__table__.name: do.__table__ for do in declarative_objects}

# sets each table as available and importable from this package.
# This way, we can import tables by
# `from datawarehouse.model import example_table_name` to get the models
[setattr(__THIS__, table_name, tables[table_name]) for table_name in tables]
