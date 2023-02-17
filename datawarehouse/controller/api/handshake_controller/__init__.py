from flask import Blueprint, request
from datawarehouse.service.handshake_service import HandshakeService

handshake_bp = Blueprint("handshake_bp", __name__, url_prefix="/prepare")


@handshake_bp.route("/", methods=["POST"])
def handshake_route():
    # See top of file for format of this json
    json = request.get_json()

    if not check_json_format(json):
        return "Invalid json format. Please check the documentation.", 500

    # TODO: handle exceptions appropriately Zac
    try:
        return HandshakeService.prepareTables(json)
    except Exception as e:
        return "Invalid hanshake", 500


def check_json_format(json):
    try:
        assert "group_name" in json
        return True
    except Exception:
        return False
