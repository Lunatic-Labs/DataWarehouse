import json
from flask import Blueprint, request, render_template

hs_bp = Blueprint(
    "hs_bp",
    __name__,
    url_prefix="/handshake",
    static_url_path="",
    template_folder="templates",
    static_folder="static",
)


@hs_bp.route("/", methods=["GET", "POST"])
def hs_func():
    if request.method == "POST":
        return render_template("handshake_post.html")
    return render_template("handshake_get.html")


if __name__ == "__main__":
    hs_bp.run()
