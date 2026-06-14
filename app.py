import logging
import os

from dotenv import load_dotenv
load_dotenv()  # Load .env file for local development BEFORE config import

from flask import Flask, flash, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import RequestEntityTooLarge

from config import Config
from extensions import csrf, limiter
from routes.admin_routes import admin_bp
from routes.event_routes import event_bp
from routes.user_routes import user_bp
from routes.volunteer_routes import volunteer_bp
from utils.helpers import ensure_database

logging.basicConfig(level=logging.INFO)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)
    limiter.init_app(app)

    ensure_database(app.config["DATABASE"])

    app.register_blueprint(user_bp)
    app.register_blueprint(volunteer_bp, url_prefix="/volunteer")
    app.register_blueprint(event_bp,     url_prefix="/events")
    app.register_blueprint(admin_bp,     url_prefix="/admin")

    # ── Security headers on every response ──────────────────────
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Frame-Options"]        = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"]       = "1; mode=block"
        response.headers["Referrer-Policy"]         = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"]      = "geolocation=(), microphone=(), camera=()"
        if app.config.get("SESSION_COOKIE_SECURE"):
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )
        return response

    @app.errorhandler(RequestEntityTooLarge)
    def handle_large_upload(error):
        flash("Uploaded file is too large. Maximum size is 5MB.", "error")
        return redirect(url_for("admin.dashboard"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")
