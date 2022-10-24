import json
from flask import Blueprint, request, render_template

hs_bp = Blueprint(
    "hs_bp",
    __name__,
    url_prefix="/handshake",
    static_url_path="",
    template_folder="templates",
    static_folder="static/stylesheets",
)

# html_handshake.static_folder = "static"


@hs_bp.route("/", methods=["GET", "POST"])
def hs_func():
    if request.method == "POST":
        data = {}
        data["class"] = request.form.get("class")
        data["group_name"] = request.form.get("group_name")
        data["src_name"] = request.form.get("src_name")
        data["metric_name"] = request.form.get("metric_name")
        data["datatype"] = request.form.get("datatype")
        data["units"] = request.form.get("units")
        data["asc"] = request.form.get("asc")
        json_data = json.dumps(data)
        return json_data
    return render_template("handshake.html")


if __name__ == "__main__":
    hs_bp.run()
