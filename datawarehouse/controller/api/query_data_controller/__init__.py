from flask import Blueprint, request

# from datawarehouse.service.query_service import QueryService

query_data_bp = Blueprint("query_data_bp", __name__, url_prefix="/query")


@query_data_bp.route("/<table_name>/")
def index(table_name):
    # service = QueryService()
    # data = service.query(table_name, request)

    breakpoint()
    return "200"


@query_data_bp.route("/a", methods=["GET", "POST"])
def i():
    return "2010"
