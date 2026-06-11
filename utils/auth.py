from functools import wraps

from flask import session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(plain_password):
    """Return a secure hash of the given plain-text password."""
    return generate_password_hash(plain_password)


def verify_password(plain_password, stored_password):
    """Return True if plain_password matches the stored hash."""
    return check_password_hash(stored_password, plain_password)


def login_required(f):
    """Decorator to require admin login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_user" not in session:
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated_function
