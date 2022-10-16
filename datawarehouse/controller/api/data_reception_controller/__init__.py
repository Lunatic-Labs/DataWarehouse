from flask import Blueprint, request

from datawarehouse.service.data_insert_service import InsertDataService

data_reception_bp = Blueprint("data_reception_bp", __name__, url_prefix="/store")


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
