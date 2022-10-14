from flask import Blueprint, request, render_template

hs_bp = Blueprint(
    "hs_bp", __name__, url_prefix="/handshake", template_folder="templates"
)


@hs_bp.route("/", methods=["GET", "POST"])
def hs_func():
    if request.method == "POST":
        name = request.form.get("name")
        number = request.form.get("number")
        return "Name: %s; Number: %s" % (name, number)
    return render_template("handshake.html")


if __name__ == "__main__":
    hs_bp.run()

    # asdklfjasld;kfj;askdjf;laskdjf asdasdf asdfasdfasdfasdf

