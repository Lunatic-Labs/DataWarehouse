from flask import Blueprint, request
from datawarehouse.service.handshake_service import HandshakeService

handshake_bp = Blueprint("interface_handshake_bp", __name__, url_prefix="/interface_prepare")
######
# 4/6/2023: Copied over directly from handshake_controller, only changed the url above.
# Just wanted to give y'all an idea of the layout for these.
# Also, not sure how much there is to be changed with this one. Seems straightforward.
#######

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
