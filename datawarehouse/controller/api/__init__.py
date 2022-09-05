from flask import Blueprint

# NOTE: Read about blueprints here https://flask.palletsprojects.com/en/1.1.x/blueprints/
# allows for having different configruations of our application.
#  For example, this will be our api side.
# If we have any frontend for some reason,
#  we will make another Blueprint and configure it accordingly.
api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/", methods=["GET"])
def index():
    return "200"
