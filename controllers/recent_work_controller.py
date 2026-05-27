import os
from uuid import uuid4

from config import Config
from models.recent_work_model import delete_recent_work, get_recent_works, insert_recent_work
from utils.validators import sanitize_filename, validate_required_fields


def get_all_recent_works():
    return get_recent_works()


def create_recent_work(form_data, image_file):
    validate_required_fields(form_data, ["title", "description"])
    if not image_file or not image_file.filename:
        raise ValueError("Recent work image is required.")

    os.makedirs(os.path.join(Config.UPLOAD_FOLDER, "recent_work_images"), exist_ok=True)
    filename = f"{uuid4().hex}_{sanitize_filename(image_file.filename)}"
    save_path = os.path.join(Config.UPLOAD_FOLDER, "recent_work_images", filename)
    image_file.save(save_path)

    insert_recent_work(
        form_data.get("title", "").strip(),
        form_data.get("description", "").strip(),
        f"uploads/recent_work_images/{filename}",
    )


def remove_recent_work(work_id):
    delete_recent_work(work_id)
