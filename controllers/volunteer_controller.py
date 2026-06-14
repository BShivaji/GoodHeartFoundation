import logging
import os
from uuid import uuid4

from config import Config
from models.volunteer_model import get_volunteers, insert_volunteer
from utils.validators import sanitize_filename, validate_required_fields

logger = logging.getLogger(__name__)

ALLOWED_DOC_EXTENSIONS = {".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png"}


MAX_DOC_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB per document


def create_volunteer(form_data, document):
    validate_required_fields(
        form_data,
        ["name", "gender", "place", "phone", "message", "area_interest"]
    )
    document_path = None

    if document and document.filename:
        _, extension = os.path.splitext(document.filename.lower())
        if extension not in ALLOWED_DOC_EXTENSIONS:
            raise ValueError(
                f"Invalid document file type '{extension}'. "
                f"Allowed: {', '.join(sorted(ALLOWED_DOC_EXTENSIONS))}"
            )

        # Check file size without fully loading into memory
        document.stream.seek(0, 2)
        file_size = document.stream.tell()
        document.stream.seek(0)

        if file_size > MAX_DOC_SIZE_BYTES:
            raise ValueError(
                "Document is too large. Maximum allowed size is 2 MB."
            )

        os.makedirs(
            os.path.join(Config.UPLOAD_FOLDER, "volunteer_docs"),
            exist_ok=True
        )
        filename  = f"{uuid4().hex}_{sanitize_filename(document.filename)}"
        save_path = os.path.join(Config.UPLOAD_FOLDER, "volunteer_docs", filename)
        document.save(save_path)
        document_path = f"uploads/volunteer_docs/{filename}"

    generated_email = (
        "volunteer_"
        + form_data.get("phone", "").strip().replace("+", "").replace("-", "")
        + "@goodheart.local"
    )

    insert_volunteer(
        form_data.get("name",          "").strip(),
        generated_email,
        form_data.get("gender",        "").strip(),
        form_data.get("place",         "").strip(),
        form_data.get("phone",         "").strip(),
        form_data.get("message",       "").strip(),
        form_data.get("area_interest", "").strip(),
        document_path,
    )


def get_all_volunteers():
    return get_volunteers()
