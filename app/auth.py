from functools import wraps
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from app.models import AuditLog, User


auth_bp = Blueprint("auth", __name__)


def can_edit_request(user) -> bool:
    return user.is_authenticated and user.role in ["admin", "agent"]


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if current_user.role not in roles:
                current_app.logger.warning("Unauthorized action attempted")
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password) and user.active:
            login_user(user)
            db.session.add(AuditLog(user_id=user.id, action="login", entity_type="user", entity_id=user.id, message=f"User {user.email} logged in"))
            db.session.commit()
            current_app.logger.info("User %s logged in", user.email)
            return redirect(url_for("main.dashboard"))

        # Bewust vrij algemene foutmelding, ook voor inactive users.
        current_app.logger.warning("Login failed for %s", email)
        flash("Login failed. Check your credentials.", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    current_app.logger.info("User %s logged out", current_user.email)
    logout_user()
    return redirect(url_for("auth.login"))
