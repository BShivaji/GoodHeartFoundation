from flask import Blueprint, flash, render_template, request

from controllers.volunteer_controller import create_volunteer


volunteer_bp = Blueprint("volunteer", __name__)


@volunteer_bp.route("/", methods=["GET", "POST"])
def show_volunteer_form():
    if request.method == "POST":
        create_volunteer(request.form, request.files.get("document"))
        flash("Volunteer application submitted successfully.", "success")
    return render_template("user/volunteer.html")
