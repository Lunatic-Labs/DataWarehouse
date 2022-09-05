"""
This controller is an example controller to showcaase the process of 
    which we will be implementing our routes/controllers. 
A controller is where we house our routes, or where you navigate to. 
    E.g. The url you put into the browser.
We will try to minimize the amount of logic we include in this, 
    and leave that to be contained in the services
SEE: datawarehouse.service.fibonacci_service
"""

from flask import request, Blueprint
from datawarehouse.service.fibonacci_service import FibonacciService
from datawarehouse.controller.api import api

fibonacci_bp = Blueprint("fibonacci_bp", __name__, url_prefix="/fibonacci")


@fibonacci_bp.route("/", methods=["GET"])
def get_number():
    index = None
    if "index" in request.args:
        index = request.args["index"]
    return str(FibonacciService.get_number(index))


# post a number, and the db will increment
#   the fibonaaci sequence by that amount of iterations.
@fibonacci_bp.route("/", methods=["POST"])
def increment_n_times():
    # the request object: read here: https://flask.palletsprojects.com/en/2.2.x/api/#flask.Request
    # contains information about the incoming request.
    # you can test this argumnet by adding a query string. eg. http://127.0.0.1:5000/api/fibonacci/?increment=1000
    # anything after a question mark is the query string.
    args = request.args
    iterate = int(args["increment"]) if "increment" in args.keys() else 1
    return_string = FibonacciService.increment_n_times(increment=iterate)
    return return_string


@fibonacci_bp.route("/reset", methods=["POST", "GET"])
def reset_fibonacci():
    FibonacciService.reset()
    return "Fibonacci sequence has been reset."
