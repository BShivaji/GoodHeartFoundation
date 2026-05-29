from flask import Flask, flash, redirect, url_for
from werkzeug.exceptions import RequestEntityTooLarge

from config import Config
from routes.admin_routes import admin_bp
from routes.event_routes import event_bp
from routes.user_routes import user_bp
from routes.volunteer_routes import volunteer_bp
from utils.helpers import ensure_database


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    ensure_database(app.config["DATABASE"])

    app.register_blueprint(user_bp)
    app.register_blueprint(volunteer_bp, url_prefix="/volunteer")
    app.register_blueprint(event_bp, url_prefix="/events")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.errorhandler(RequestEntityTooLarge)
    def handle_large_upload(error):
        flash("Uploaded file is too large. Maximum size is 5MB.", "error")
        return redirect(url_for("admin.dashboard"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
