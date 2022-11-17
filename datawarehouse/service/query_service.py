from sqlalchemy import and_, text, or_
import collections
from datawarehouse.service import BaseService
from datawarehouse.config.db import config as db
from stringcase import spinalcase

DEFAULT_OPERATOR = "=="

# NOTE: This currently requires that you pass in the metric uid to query the data. not the column name.


op_to_sa_op = {
    "<": "__lt__",
    "<<": "__le__",
    DEFAULT_OPERATOR: "__eq__",
    "eq": "__eq__",
    "!": "__ne__",
    ">>": "__ge__",
    ">": "__gt__",
    "like": "ilike",
    "contains": "contains",
    "contained_by": "contained_by",
}
op_to_array_op = {"contains": "@>", "contained_by": "<@"}


def clause_from_str(col, op, values):
    op = op_to_sa_op[op]
    col_name = f"{col.table.schema}.{str(col)}"
    if op == "ilike":
        values = [f"%{value}" for value in values]
    else:
        pass
    col_op = getattr(col, op)
    if op in ["__ne__"] + list(op_to_array_op.keys()):
        combinator = and_
    else:
        combinator = or_
    return combinator(*[col_op(value) for value in values])


def clause_from_default(col, op, values):
    col_op = getattr(col, op_to_sa_op[op])
    return or_(*[col_op(value) for value in values])


def clause_from_list(col, op, values):
    col_op = op_to_sa_op[op]
    col_name = f"{col.table.schema}.{str(col)}"
    if col_op == op_to_sa_op[DEFAULT_OPERATOR]:
        return or_(*[text(f"{col_name}::TEXT ILIKE '%{value}%'") for value in values])
    elif op in op_to_array_op:
        arr_col_op = op_to_array_op[op]
        pg_values = "'{" + ",".join([f'"{value}"' for value in values]) + "}'"
        return and_(text(f"{col_name} {arr_col_op} {pg_values}"))
    else:
        raise Exception(f"{op} is not a valid operator for list type columns")


clause_map = {str: clause_from_str, list: clause_from_list}


class QueryService(BaseService):

    session = db.session

    @classmethod
    def query(self, table_name, request):
        table = self._get_table(table_name)  # get the table object
        qry = self.session.query(table)  # create a base query object on the table
        criteria = self.criteria_for_request(
            request, table
        )  # extract the query criteria from the request query string

        qry = self.apply_kw_criteria(qry, table, **criteria)
        # TODO: implement the rest of this https://github.com/cordata/watchtower/blob/develop/watchtower/blueprints/__init__.py
        return qry.all()

    def criteria_for_request(self, request, table):

        attrs = table.c.keys()
        criteria_keys = [
            k for k in request.args.keys() if self.parse_qry_param(k)[0] in attrs
        ]

        def as_default(criteria_key, model):
            name, op = self.parse_qry_param(criteria_key)
            col_type = self.get_effective_col_type(model.c[name])
            if col_type is str and op == "==":
                return f"{criteria_key}__like"
            else:
                return criteria_key

        def maybe_null(v):
            if v and str(v).lower() == "null":
                return None
            else:
                return v

        return {
            as_default(k, table): [maybe_null(x) for x in request.args.getlist(k)]
            for k in criteria_keys
        }

    def parse_qry_param(q):
        # tokenize the query string, get the operators and the name to filter by
        # Format: `col__<`
        # the above will return ["col", "<"]
        try:
            [name, op] = q.rsplit("__", 1)
            return [name, op]
        except ValueError:
            return [q, DEFAULT_OPERATOR]

    def get_effective_col_type(col):
        try:
            return col.type.python_type
        except NotImplementedError:
            return col.type

    def apply_kw_criteria(self, qry, table, **criteria):
        return qry.filter(*self.criteria_to_clauses(table, **criteria))

    def ensure_collection(self, values):
        if type(values) in [str, bytes]:
            return [values]
        else:
            if isinstance(values, collections.Iterable):
                return [values]

    def query_clause(self, col, op, values):
        clause_from = clause_map.get(
            self.get_effective_col_type(col), clause_from_default
        )
        v = self.ensure_collection(values)
        return clause_from(col, op, v)

    def criteria_to_clauses(self, table, **criteria):
        m = table.c
        params = (self.parse_qry_param(k) + [values] for k, values in criteria.items())
        return [
            self.qry_clause(getattr(m, col_name), op, values)
            for col_name, op, values in params
        ]
