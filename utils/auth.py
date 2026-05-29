from functools import wraps
from flask import session, redirect, url_for


def verify_password(plain_password, stored_password):
    return plain_password == stored_password


def login_required(f):
    """Decorator to require admin login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_user" not in session:
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated_function
