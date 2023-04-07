from flask import Blueprint, request

from datawarehouse.service.data_insert_service import InsertDataService

data_reception_bp = Blueprint("interface_data_reception_bp", __name__, url_prefix="/interface_store")
######
# 4/6/2023: Copied over directly from data_reception_controller, only changed the url above.
# Just wanted to give y'all an idea of the layout for these.
#######

@data_reception_bp.route("/", methods=["POST"])
def store_data():
    json = request.json
    service = InsertDataService()
    # implement this eventually
    err = service.verifyInformation(json)
    if err:
        return err

    service.addData(json)
    return "success", 200
