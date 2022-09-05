from datawarehouse.config.db import config as db
from datawarehouse.model import fibonacci
from datawarehouse.service import BaseService

from sqlalchemy import func, insert


class FibonacciService(BaseService):

    session = db.session

    @classmethod
    def get_last_id(self):
        last_id = self.session.query(func.max(fibonacci.c.id)).scalar()
        return last_id

    @classmethod
    def get_number(self, index=0):
        id = index or self.session.query(func.max(fibonacci.c.id)).scalar()
        return (
            self.session.query(fibonacci.c.number)
            .where(fibonacci.c.id == id)
            .first()
            .number
        )

    @classmethod
    def increment_n_times(self, increment=1):
        for i in range(increment):
            last_id = self.get_last_id()
            last_no = self.get_number(last_id)
            sec_last_no = self.get_number(last_id - 1) if last_id > 1 else 0
            stmt = insert(fibonacci).values(number=last_no + sec_last_no)
            # self.session.begin()

            self.session.execute(stmt)
            self.session.commit()
