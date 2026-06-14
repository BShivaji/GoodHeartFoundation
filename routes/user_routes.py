import logging
import os
import random
import re
from datetime import date

from flask import Blueprint, render_template, request, flash, redirect, url_for

from controllers.recent_work_controller import get_all_recent_works
from utils.helpers import fetch_one, fetch_all
from extensions import limiter

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
@limiter.limit("5 per minute; 20 per hour")
def contact():
    if request.method == "POST":
        # Sanitize and length-cap all inputs
        name    = request.form.get("name",    "").strip()[:100]
        email   = request.form.get("email",   "").strip()[:150]
        subject = request.form.get("subject", "").strip()[:200]
        message = request.form.get("message", "").strip()[:2000]
        phone   = request.form.get("phone",   "").strip()[:20]

        # Validate required fields
        if not name:
            flash("Name is required.", "error")
            return redirect(url_for("user.contact"))

        if not message:
            flash("Message is required.", "error")
            return redirect(url_for("user.contact"))

        # Validate email format
        email_pattern = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
        if not email or not email_pattern.match(email):
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("user.contact"))

        from utils.helpers import execute_query
        execute_query(
            """
            INSERT INTO contact_messages
                (name, email, phone, subject, message)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, email, phone, subject, message),
        )

        logger.info("Contact form submitted by: %s <%s>", name, email)
        flash(
            "Your message has been sent successfully! "
            "Our team will get back to you soon.",
            "success"
        )
        return redirect(url_for("user.contact"))

    return render_template("user/contact.html")
