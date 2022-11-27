from flask import Blueprint, request, render_template

abc_bp = Blueprint("abc_bp", __name__, url_prefix="/abc", template_folder="templates")


@abc_bp.route("/", methods=["GET", "POST"])
def abc_func():
    if request.method == "POST":
        name = request.form.get("name")
        number = request.form.get("number")
        return "Name: %s; Number: %s" % (name, number)
    return render_template("abc.html")


if __name__ == "__main__":
    abc_bp.run()
