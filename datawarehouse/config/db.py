import sys, logging, os
from sqlalchemy import create_engine, orm, schema, inspect, event

# from zope.sqlalchemy  import register
log = logging.getLogger(__name__)
__THIS__ = sys.modules[__name__]

Session = orm.scoped_session(orm.session_maker())
# register(Session)
metadata = schema.MetaData()


def make_engine(db_url, pool_size=5, max_overflow=10):
    engine = create_engine(db_url, pool_size=pool_size, max_overflow=max_overflow)
    return engine


class DBConfig(object):
    def __init__(self, **settings):
        log.debug(f"initializing {__name__} with settings {settings}")

        self.__dict__ = {**self.__dict__, **settings}
        self._settings = settings
        self._engine = make_engine(settings["db_url"])
        self._scoped_session_factory = Session
        self._scoped_session_factory.configure(bind=self._engine)
        self._meta = metadata
        self._meta.bind = self._engine
        self._inspector = inspect(self._engine)

    def update_meta(self, new_meta):
        self._meta = new_meta

    @property
    def engine(self):
        return self._engine

    @property
    def inspector(self):
        return self._inspector

    @property
    def meta(self):
        return self._meta

    @property
    def session(self):
        return self._scoped_session_factory()


settings = {"db_url": os.environ.get("DATABASE_URL")}
config = DBConfig(**settings)
setattr(__THIS__, "config", config)
