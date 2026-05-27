import re


def validate_required_fields(form_data, fields):
    missing_fields = [field for field in fields if not form_data.get(field, "").strip()]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")


def sanitize_filename(filename):
    return re.sub(r"[^A-Za-z0-9._-]", "_", filename)
