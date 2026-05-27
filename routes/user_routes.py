import os
import random

from flask import Blueprint, render_template

from controllers.recent_work_controller import get_all_recent_works


user_bp = Blueprint("user", __name__)


@user_bp.route("/")
def home():
    achievements_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "static",
        "images",
        "acheivements",
    )
    achievement_images = []
    allowed_extensions = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

    if os.path.isdir(achievements_dir):
        for filename in sorted(os.listdir(achievements_dir)):
            _, extension = os.path.splitext(filename.lower())
            if extension in allowed_extensions:
                achievement_images.append(
                    {
                        "title": os.path.splitext(filename)[0].replace("_", " ").replace("-", " ").title(),
                        "image": f"images/acheivements/{filename}",
                    }
                )

    return render_template(
        "user/index.html",
        achievement_images=achievement_images,
        recent_works=get_all_recent_works(),
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
