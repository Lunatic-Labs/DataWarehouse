from sqlalchemy import Table
from datawarehouse.config.db import config as db

"""
funciton get_table(name)
If the table exists, it will return the table object. otherwise, it will return false
"""


def get_table(name):
    if name in db.meta.tables:
        table = Table(
            name,
            db.meta,
            autoload=True,
            autoload_with=db.engine,
            keep_existing=True,
        )
        return table
    return None


"""
function drop_table(name)
given a source_uid, the function will drop the table if it exists. 
"""


def drop_table(name):
    table = get_table(name=name)
    if table is not None:
        table.drop()
