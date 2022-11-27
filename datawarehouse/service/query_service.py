from sqlalchemy import and_, text, or_
import collections.abc as collections
from datawarehouse.service import BaseService
from datawarehouse.config.db import config as db

DEFAULT_OPERATOR = "=="

# NOTE: This currently requires that you pass in the metric uid to query the data. not the column name.

# this is all the supported operations that can be used to query the db.
# all of the keys in this dict are what you would pass in, prepended by two underscores.
# e.g. "__<" will evaluate to a less-than operation.
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

excluded_cols = ["pk", "timestamp"]


""" function takes in column, operation, and values and returns a sqlalchemy clause for the operation"""


def clause_from_str(col, op, values):
    op = op_to_sa_op[op]
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


""" function takes in column, operation, and values and returns a sqlalchemy clause for the operation"""


def clause_from_default(col, op, values):
    col_op = getattr(col, op_to_sa_op[op])
    return or_(*[col_op(value) for value in values])


""" function takes in column, operation, and values and returns a sqlalchemy clause for the operation"""


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

"""
Class for querying the database through a request object.
USAGE:
the query() method is the only public method. takes in a table to query from, a request object, and a limit for rows desired. 
builds a query object with the given filtering criteria, and returns the results.
"""


class QueryService(BaseService):

    session = db.session

    """Method takes in a table name, and the request object from the controller
    The request object allows it to get the query string, which it tokenizes (criteria_for_request),
    then applys those tokenized criteria to the query object"""

    def query(self, table_name, request, limit=1000):
        table = self._get_table(table_name)  # get the table object
        qry = self.session.query(table)  # create a base query object on the table
        criteria = self._criteriaForRequest(
            request=request, table=table
        )  # extract the query criteria from the request query string

        qry = self._applyKWCriteria(qry, table, **criteria)

        rslt = qry.order_by(table.c.timestamp.desc()).limit(limit).all()
        return rslt

    def _getTableUserDefinedColNames(self, table):
        metric = self._get_table("metric")
        metric_names = (
            self.session.query(metric.c.name)
            .where(
                metric.c.metric_uid.in_(
                    [k for k in table.c.keys() if k not in excluded_cols]
                )
            )
            .all()
        )
        metric_names = [k.name for k in metric_names]
        return metric_names

    # replaces a user-defined query criteria with the valid metric uid for the source.
    def _colNameToUID(self, request, col_name):
        source_uid = request.view_args["source_uid"]
        metric_table = self._get_table("metric")
        col_name, op = self._parseQryParam(col_name)
        if col_name not in excluded_cols:
            return (
                self.session.query(metric_table.c.metric_uid)
                .where(
                    and_(
                        metric_table.c.source_uid == source_uid,
                        metric_table.c.name == col_name,
                    )
                )
                .scalar()
                + "__"
                + op
            )

        else:
            return col_name + "__" + op

    """ Takes in a request object, and the SA table object
    finds which of the request query string parameters apply to this particular table, ignores the rest
    returns a dict of critera strings to filter value. 
    e.g. {"temperature__eq": 98.6}
    """

    def _criteriaForRequest(self, request, table):
        attrs = table.c.keys()
        col_names = self._getTableUserDefinedColNames(table)
        # identify the columns that they are filtering by and the operation

        criteria_keys = [
            k
            for k in request.args.keys()
            if self._parseQryParam(k)[0] in [*attrs, *col_names]
        ]

        # applys a "like" operation to strings
        def as_default(criteria_key, model):
            name, op = self._parseQryParam(criteria_key)
            col_type = self._getEffectiveColType(model.c[name])
            if col_type is str and op == "==":
                return f"{criteria_key}__like"
            else:
                return criteria_key

        # if the user is looking for a null, this allows that.
        def maybe_null(v):
            if v and str(v).lower() == "null":
                return None
            else:
                return v

        # change user-defined column names into the metric uid for querying if necessary.
        return {
            as_default(
                self._colNameToUID(request, k)
                if self._parseQryParam(k)[0] in col_names
                else k,
                table,
            ): [maybe_null(x) for x in request.args.getlist(k)]
            for k in criteria_keys
        }

    """tokenizes a query criteria. distinguishes between the column name and the operator"""

    def _parseQryParam(self, q):
        # tokenize the query string, get the operators and the name to filter by
        # Format: `col__<`
        # the above will return ["col", "<"]
        try:
            [name, op] = q.rsplit("__", 1)
            # if we are using metric_uids to query, great. Otherwise, we need to gather the correct metric_uid to query

            return [name, op]
        except ValueError:
            return [q, DEFAULT_OPERATOR]

    """takes a SA column, returns the type that the column is in python"""

    def _getEffectiveColType(self, col):
        try:
            return col.type.python_type
        except NotImplementedError:
            return col.type

    """applies the criteria to a query object"""

    def _applyKWCriteria(self, qry, table, **criteria):
        return qry.filter(*self._criteriaToClauses(table, **criteria))

    # just ensures that the values are in a collection type, not just the value alone. generalizes handling multiple vs one value
    def _ensureCollection(self, values):
        if type(values) in [str, bytes]:
            return [values]
        else:
            if isinstance(values, collections.Iterable):
                return values
            else:
                return [values]

    """ Builds out a query clause based on the type of the values. If the type is a string/list, its handled differently.
    all other types are handled by `clause_from_default`"""

    def _queryClause(self, col, op, values):
        clause_from = clause_map.get(
            self._getEffectiveColType(col), clause_from_default
        )
        v = self._ensureCollection(values)
        return clause_from(col, op, v)

    """converts the query criteria to a clause to be applied to a query object. """

    def _criteriaToClauses(self, table, **criteria):
        m = table.c
        params = (self._parseQryParam(k) + [values] for k, values in criteria.items())
        return [
            self._queryClause(getattr(m, col_name), op, values)
            for col_name, op, values in params
        ]
