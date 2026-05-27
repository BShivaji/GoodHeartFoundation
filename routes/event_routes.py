from flask import Blueprint, render_template

from controllers.event_controller import get_all_events


event_bp = Blueprint("event", __name__)


@event_bp.route("/")
def list_events():
    return render_template("user/events.html", events=get_all_events())
