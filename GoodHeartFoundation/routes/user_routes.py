import os

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
    gallery_items = [
        {"title": "Community Meal Drive", "image": "https://via.placeholder.com/600x400?text=Meal+Drive"},
        {"title": "Education Support", "image": "https://via.placeholder.com/600x400?text=Education"},
        {"title": "Health Camp", "image": "https://via.placeholder.com/600x400?text=Health+Camp"},
    ]
    return render_template("user/gallery.html", gallery_items=gallery_items)
