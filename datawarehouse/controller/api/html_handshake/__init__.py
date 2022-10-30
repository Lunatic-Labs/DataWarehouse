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


@hs_bp.route("/", methods=["GET", "POST"])
def hs_func():
    if request.method == "POST":
        data = {}
        data["class"] = request.form.get("class")
        data["group_name"] = request.form.get("group_name")
        data["src_name"] = request.form.get("src_name")
        data["metric_name"] = request.form.get("metric_name")
        # print(request.form.getlist("metric_name"))
        data["datatype"] = int(request.form.get("datatype"))
        data["units"] = request.form.get("units")
        data["asc"] = request.form.get("asc")
        json_data = json.dumps(data, indent=4)
        # print(json_data)
        return json_data
    return render_template("handshake.html")


if __name__ == "__main__":
    hs_bp.run()
