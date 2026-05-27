from models.event_model import delete_event, get_events, insert_event, update_event_date
from utils.validators import validate_required_fields


def create_event(form_data):
    validate_required_fields(form_data, ["title", "event_date", "location"])
    insert_event(
        form_data.get("title", "").strip(),
        form_data.get("description", "").strip(),
        form_data.get("event_date", "").strip(),
        form_data.get("location", "").strip(),
    )


def get_all_events():
    return get_events()


def edit_event_date(event_id, form_data):
    validate_required_fields(form_data, ["event_date"])
    update_event_date(event_id, form_data.get("event_date", "").strip())


def remove_event(event_id):
    delete_event(event_id)
