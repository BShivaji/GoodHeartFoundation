from flask import Blueprint, render_template, request
from controllers.event_controller import get_all_events

event_bp = Blueprint("event", __name__)

@event_bp.route("/")
def list_events():
    events      = get_all_events()
    search_query = request.args.get("q", "").strip()

    if search_query:
        lowered = search_query.lower()
        events  = [
            e for e in events
            if lowered in (
                e.get("title",       "")
                + e.get("location",  "")
                + e.get("description", "")
            ).lower()
        ]

    return render_template(
        "user/events.html",
        events=events,
        search_query=search_query
    )
