from uuid import UUID
from sqlalchemy import Table

from datawarehouse.config.db import config as db


class BaseService:
    _engine = db.engine
    _connection = _engine.connect()
    _metadata_obj = db.meta

    @classmethod
    def _checkUUIDFormat(self, uuid):
        try:
            UUID(uuid, version=4)
        except:
            return False
        return True

    @classmethod
    def _get_table(self, source_uid):

        table = Table(
            source_uid,
            self._metadata_obj,
            autoload=True,
            autoload_with=self._engine,
            keep_existing=True,
        )
        return table
