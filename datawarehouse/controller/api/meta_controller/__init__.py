from flask import Blueprint , request
from datawarehouse.service.meta_service import MetaService
meta_bp = Blueprint('meta_bp', __name__, url_prefix="/meta")

@meta_bp.route("/", methods=["GET"])
def index():
    service = MetaService();

    return service.get_metadata(uids=request.json)