from flask import Blueprint, request

from datawarehouse.service.query_service import QueryService
from datawarehouse.service.meta_service import MetaService

query_data_bp = Blueprint("query_data_bp", __name__, url_prefix="/query")


@query_data_bp.route("/<group_uid>/<source_uid>/", methods=["GET"])
def index(group_uid, source_uid):
    service = QueryService()
    meta_service = MetaService()

    if not meta_service.ensure_group_ownership_of_source(group_uid, source_uid):
        return dict(
            error="this combination of source and group are not in our database."
        )
    limit = request.args["limit"] if "limit" in request.args.keys() else None
    data = service.query(source_uid, request, limit)
    # change the uid column names into the user-defined column names
    data = {x: data[x]._asdict() for x in range(len(data))}
    for x in data:
        keys = list(data[x].keys())
        for metric in keys:
            if metric != "timestamp":
                col_name = meta_service.get_name_from_uid("metric", metric)
                data[x][col_name] = data[x].pop(metric)

    return data
