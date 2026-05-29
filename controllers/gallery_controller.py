import os
from uuid import uuid4

from utils.validators import sanitize_filename

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def _gallery_dir():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "images", "gallery")


def _ensure_gallery_dir():
    directory = _gallery_dir()
    os.makedirs(directory, exist_ok=True)
    return directory


def get_gallery_photos():
    gallery_dir = _gallery_dir()
    gallery_items = []

    if os.path.isdir(gallery_dir):
        for filename in sorted(os.listdir(gallery_dir)):
            _, extension = os.path.splitext(filename.lower())
            if extension in ALLOWED_EXTENSIONS:
                gallery_items.append({"filename": filename, "image": f"images/gallery/{filename}"})

    return gallery_items


def save_gallery_photo(image_file):
    if not image_file or not image_file.filename:
        raise ValueError("Gallery image is required.")

    _, extension = os.path.splitext(image_file.filename.lower())
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid gallery image file type.")

    gallery_dir = _ensure_gallery_dir()
    filename = f"{uuid4().hex}_{sanitize_filename(image_file.filename)}"
    save_path = os.path.join(gallery_dir, filename)
    image_file.save(save_path)


def remove_gallery_photo(filename):
    if not filename:
        return

    safe_filename = sanitize_filename(filename)
    gallery_dir = _gallery_dir()
    file_path = os.path.join(gallery_dir, safe_filename)

    if os.path.isfile(file_path):
        os.remove(file_path)
