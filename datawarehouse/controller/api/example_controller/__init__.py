from email.policy import default
from flask import Blueprint, request

from datawarehouse.service.example_service import ExampleService

# a blueprint is an instance of the application.
# It can have its own logic, routes, services,
# properties, authentication requirements, you name it.
example_bp = Blueprint("example_bp", __name__, url_prefix="/datadogs")

# This is an example of a route that just returns some text.
# If you navigate to `/api/datadogs/`, you will see the returned value.
@example_bp.route("/", methods=["GET", "POST"])
def get_request():
    return "Hello Worlds ashdfasdfga"


# this route can be found at `/api/datadogs/sub-route/`.
# it also only supports GET http requests.
# If you send a POST request here, it will not succeed.
@example_bp.route("/sub-route", methods=["GET"])
def sub_route():
    return "This is a subroute"

    """There are many ways to pass data from the client to the server.
    You can pass arguemnts into the url, or you can include data in a header or request body.
    """


# This route has an argument in the url (inside the <>) it is declaared to be an int.
# this route will be found at /api/datadogs/add1/<int argument>, and only supports GET http req.
# if you dont provide an argument, it is defaulted to 1
@example_bp.route("/add1/<int:arg1>", methods=["GET"])
@example_bp.route("/add1/", methods=["GET"], defaults={"arg1": 1})
def add_one_to_the_arg(arg1):
    return str(arg1 + 1)


# This route will return any arguemnts that are defined in the url after the query string
# a query string is a series of key-value pairs that follow the `?` character in a url.
# for example : `/api/datadogs/query-string?key=value&key1=value1`
# you can have multiple query string arguments and split them by using a `&` character.
# just google "url query string" for more info
# read more about the requset object here https://tedboy.github.io/flask/generated/generated/flask.Request.html
@example_bp.route("/query-string", methods=["GET", "POST"])
def query_string():
    args = request.args
    return args


# this route uses the request object to get data from the client.
# it uses the `request.json` attribute to get the json data thats passed into the http request.
# read more about the requset object here https://tedboy.github.io/flask/generated/generated/flask.Request.html
@example_bp.route("/request-body-data", methods=["GET", "POST"])
def request_body_data():
    json = request.json
    return json


"""The following route will invoke the ExampleService class. 
All of the previous routes did not use this service.
 Any heavy logic (eg. accessing the database, interacting with other services... etc)
 will find itself not in the route (or controller file, this file) but rather in the Service files. 
"""


@example_bp.route("/service_demo/<int:seed>", methods=["GET", "POST"])
@example_bp.route("/service_demo", methods=["GET", "POST"], defaults={"seed": 1})
def service_demo(seed):
    service = ExampleService()
    data = service.getRandomInt(seed)
    return str(data)


# YOU should try to write a route that implements the ExampleService, and use its getRandomEvenInt() class method to get a number and return it to the client. Give it a try!
