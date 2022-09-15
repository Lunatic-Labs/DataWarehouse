from flask import Blueprint

example_bp = Blueprint("example_bp", __name__, url_prefix="/datadogs")


@example_bp.route("/", methods=["GET", "POST"])
def get_request():
    return "Hello Worlds ashdfasdfga"
