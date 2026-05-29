from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from controllers.admin_controller import build_dashboard_stats, check_admin_login
from controllers.expenditure_controller import (
    create_expenditure,
    edit_expenditure,
    get_expenditure_summary,
    remove_expenditure,
)
from controllers.event_controller import create_event, edit_event_date, get_all_events, remove_event
from controllers.fund_controller import create_fund, edit_fund, get_fund_summary, remove_fund
from controllers.recent_work_controller import create_recent_work, get_all_recent_works, remove_recent_work
from controllers.gallery_controller import get_gallery_photos, save_gallery_photo, remove_gallery_photo
from controllers.volunteer_controller import get_all_volunteers


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if check_admin_login(request.form.get("username"), request.form.get("password")):
            session["admin_user"] = request.form.get("username")
            return redirect(url_for("admin.dashboard"))
        flash("Invalid credentials", "error")
    return render_template("admin/login.html")


@admin_bp.route("/dashboard")
def dashboard():
    recent_works = []
    gallery_items = []

    try:
        recent_works = get_all_recent_works()
    except Exception:
        flash("Unable to load recent works. Please refresh the page.", "error")

    try:
        gallery_items = get_gallery_photos()
    except Exception:
        flash("Unable to load gallery images. Please refresh the page.", "error")

    return render_template(
        "admin/dashboard.html",
        stats=build_dashboard_stats(),
        recent_works=recent_works,
        gallery_items=gallery_items,
    )


@admin_bp.route("/volunteers")
def manage_volunteers():
    volunteers = get_all_volunteers()
    search_query = request.args.get("q", "").strip()

    if search_query:
        lowered_query = search_query.lower()
        volunteers = [
            volunteer
            for volunteer in volunteers
            if lowered_query in " ".join(
                [
                    str(volunteer.get("name", "")),
                    str(volunteer.get("gender", "")),
                    str(volunteer.get("place", "")),
                    str(volunteer.get("phone", "")),
                    str(volunteer.get("area_interest", "")),
                    str(volunteer.get("message", "")),
                    str(volunteer.get("email", "")),
                ]
            ).lower()
        ]

    return render_template(
        "admin/volunteers.html",
        volunteers=volunteers,
        search_query=search_query,
    )


@admin_bp.route("/add-events", methods=["GET", "POST"])
def add_events():
    if request.method == "POST":
        create_event(request.form)
        return redirect(url_for("admin.manage_events"))
    return render_template("admin/add_events.html")


@admin_bp.route("/manage-events")
def manage_events():
    events = get_all_events()
    search_query = request.args.get("q", "").strip()
    today = date.today()

    for event in events:
        try:
            event_date = date.fromisoformat(event.get("event_date", ""))
            event["status"] = "Upcoming" if event_date >= today else "Completed"
        except ValueError:
            event["status"] = "Unknown"

    if search_query:
        lowered_query = search_query.lower()
        events = [
            event
            for event in events
            if lowered_query in " ".join(
                [
                    str(event.get("title", "")),
                    str(event.get("event_date", "")),
                    str(event.get("location", "")),
                    str(event.get("description", "")),
                    str(event.get("status", "")),
                ]
            ).lower()
        ]

    return render_template(
        "admin/manage_events.html",
        events=events,
        search_query=search_query,
    )


@admin_bp.route("/events/<int:event_id>/update-date", methods=["POST"])
def update_event_date(event_id):
    edit_event_date(event_id, request.form)
    return redirect(url_for("admin.manage_events"))


@admin_bp.route("/events/<int:event_id>/delete", methods=["POST"])
def delete_event(event_id):
    remove_event(event_id)
    return redirect(url_for("admin.manage_events"))


@admin_bp.route("/funds")
def funds():
    funds_summary = get_fund_summary()
    search_query = request.args.get("q", "").strip()

    if search_query:
        lowered_query = search_query.lower()
        funds_summary["donors"] = [
            donor
            for donor in funds_summary["donors"]
            if lowered_query in " ".join(
                [
                    str(donor.get("donor_name", "")),
                    str(donor.get("created_at", "")),
                    str(donor.get("amount", "")),
                    str(donor.get("purpose", "")),
                ]
            ).lower()
        ]

    return render_template("admin/funds.html", funds=funds_summary, search_query=search_query)


@admin_bp.route("/add-donor", methods=["POST"])
def add_donor():
    create_fund(request.form)
    return redirect(url_for("admin.funds"))


@admin_bp.route("/funds/<int:fund_id>/update", methods=["POST"])
def update_donor(fund_id):
    edit_fund(fund_id, request.form)
    return redirect(url_for("admin.funds"))


@admin_bp.route("/funds/<int:fund_id>/delete", methods=["POST"])
def delete_donor(fund_id):
    remove_fund(fund_id)
    return redirect(url_for("admin.funds"))


@admin_bp.route("/expenditures")
def expenditures():
    expenditure_summary = get_expenditure_summary()
    search_query = request.args.get("q", "").strip()

    if search_query:
        lowered_query = search_query.lower()
        expenditure_summary["records"] = [
            record
            for record in expenditure_summary["records"]
            if lowered_query in " ".join(
                [
                    str(record.get("event_name", "")),
                    str(record.get("created_at", "")),
                    str(record.get("amount", "")),
                    str(record.get("purpose", "")),
                ]
            ).lower()
        ]

    return render_template(
        "admin/expenditures.html",
        expenditures=expenditure_summary,
        search_query=search_query,
    )


@admin_bp.route("/add-expenditure", methods=["POST"])
def add_expenditure():
    create_expenditure(request.form)
    return redirect(url_for("admin.expenditures"))


@admin_bp.route("/expenditures/<int:expenditure_id>/update", methods=["POST"])
def update_expenditure(expenditure_id):
    edit_expenditure(expenditure_id, request.form)
    return redirect(url_for("admin.expenditures"))


@admin_bp.route("/expenditures/<int:expenditure_id>/delete", methods=["POST"])
def delete_expenditure(expenditure_id):
    remove_expenditure(expenditure_id)
    return redirect(url_for("admin.expenditures"))


@admin_bp.route("/logout")
def logout():
    session.pop("admin_user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("user.home"))


@admin_bp.route("/recent-works", methods=["POST"])
def add_recent_work():
    try:
        create_recent_work(request.form, request.files.get("image"))
        flash("Recent work posted successfully.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    except Exception:
        flash("Unable to add recent work. Please try again.", "error")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/gallery-photos", methods=["POST"])
def add_gallery_photo():
    try:
        save_gallery_photo(request.files.get("image"))
        flash("Gallery photo uploaded successfully.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    except Exception:
        flash("Unable to upload gallery photo. Please try again.", "error")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/gallery-photos/<filename>/delete", methods=["POST"])
def delete_gallery_photo(filename):
    try:
        remove_gallery_photo(filename)
        flash("Gallery photo deleted successfully.", "success")
    except Exception:
        flash("Unable to delete gallery photo. Please try again.", "error")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/recent-works/<int:work_id>/delete", methods=["POST"])
def delete_recent_work(work_id):
    try:
        remove_recent_work(work_id)
        flash("Recent work deleted successfully.", "success")
    except Exception:
        flash("Unable to delete recent work. Please try again.", "error")
    return redirect(url_for("admin.dashboard"))
