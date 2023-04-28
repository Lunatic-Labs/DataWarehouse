from flask import Blueprint, request

from datawarehouse.service.interface_data_insert_service import InterfaceInsertDataService

data_reception_bp = Blueprint("interface_data_reception_bp", __name__, url_prefix="/interface_store")
######
# 4/6/2023: Copied over directly from data_reception_controller, only changed the url above.
# Just wanted to give y'all an idea of the layout for these.
#######

@data_reception_bp.route("/", methods=["POST"])
def store_data():
    #how to receive data from interface?
    # json = request.json
    data = request.data.decode()
    print(f"DATA: {data}")
    service = InterfaceInsertDataService() #InterfaceInsertDataService() class that has a function for converting data from interface into a JSON-formatted string. 
    json = service.dataToJSON(data) #call with passed data
    print(f"JSON: {json}")
    # implement this eventually
    # err = service.verifyInformation(json)   #Either verify data or verify the created .json
    # if err:
    #     return err


    service.addData(json)
    return "success", 200
