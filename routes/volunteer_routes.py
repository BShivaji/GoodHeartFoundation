import logging

from flask import Blueprint, flash, render_template, request

from controllers.volunteer_controller import create_volunteer

logger = logging.getLogger(__name__)

volunteer_bp = Blueprint("volunteer", __name__)


@volunteer_bp.route("/", methods=["GET", "POST"])
def show_volunteer_form():
    if request.method == "POST":
        try:
            create_volunteer(request.form, request.files.get("document"))
            flash("Volunteer application submitted successfully.", "success")
        except ValueError as exc:
            flash(str(exc), "error")
        except Exception:
            logger.exception("Volunteer form submission failed")
            flash("Something went wrong. Please try again later.", "error")
    return render_template("user/volunteer.html")
