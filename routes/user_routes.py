import logging
import os
import random
from datetime import date

from flask import Blueprint, render_template, request, flash, redirect, url_for

from controllers.recent_work_controller import get_all_recent_works
from utils.helpers import fetch_one, fetch_all

logger = logging.getLogger(__name__)

user_bp = Blueprint("user", __name__)


@user_bp.route("/")
def home():
    gallery_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "static",
        "images",
        "gallery",
    )
    achievement_images = []
    allowed_extensions = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

    if os.path.isdir(gallery_dir):
        for filename in sorted(os.listdir(gallery_dir)):
            _, extension = os.path.splitext(filename.lower())
            if extension in allowed_extensions:
                achievement_images.append(
                    {
                        "title": os.path.splitext(filename)[0].replace("_", " ").replace("-", " ").title(),
                        "image": f"images/gallery/{filename}",
                    }
                )

    # Fetch real stats from the database
    today = date.today().isoformat()

    volunteer_row = fetch_one("SELECT COUNT(*) AS cnt FROM volunteers")
    volunteer_count = volunteer_row["cnt"] if volunteer_row else 0

    events_row = fetch_one(
        "SELECT COUNT(*) AS cnt FROM events WHERE event_date >= ?", (today,)
    )
    upcoming_events = events_row["cnt"] if events_row else 0

    funds_row = fetch_one("SELECT COALESCE(SUM(amount), 0) AS total FROM funds")
    total_raised = funds_row["total"] if funds_row else 0

    return render_template(
        "user/index.html",
        achievement_images=achievement_images,
        recent_works=get_all_recent_works(),
        volunteer_count=volunteer_count,
        upcoming_events=upcoming_events,
        total_raised=total_raised,
    )


@user_bp.route("/gallery")
def gallery():
    gallery_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "static",
        "images",
        "gallery",
    )
    gallery_items = []
    allowed_extensions = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

    if os.path.isdir(gallery_dir):
        for filename in os.listdir(gallery_dir):
            _, extension = os.path.splitext(filename.lower())
            if extension in allowed_extensions:
                gallery_items.append(
                    {"image": f"images/gallery/{filename}"}
                )
    
    # Randomize the order
    random.shuffle(gallery_items)
    
    return render_template("user/gallery.html", gallery_items=gallery_items)


@user_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        
        from utils.helpers import execute_query
        execute_query(
            "INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)",
            (name, email, subject, message)
        )
        
        flash("Your message has been sent successfully! Our team will get back to you soon.", "success")
        return redirect(url_for("user.contact"))
        
    return render_template("user/contact.html")
