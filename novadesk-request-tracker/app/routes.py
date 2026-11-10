from time import sleep

from flask import Blueprint, abort, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.auth import can_edit_request, role_required
from app.models import SupportRequest, User
from app.services import create_support_request, get_dashboard_stats, search_requests, update_support_request


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    stats = get_dashboard_stats()
    return render_template("dashboard.html", stats=stats)


@main_bp.route("/requests")
@login_required
def requests_list():
    support_requests = SupportRequest.query.order_by(SupportRequest.created_at.desc()).all()
    return render_template("requests.html", support_requests=support_requests)


@main_bp.route("/requests/search")
@login_required
def requests_search():
    q = request.args.get("q", "")
    results = search_requests(q)
    return render_template("requests.html", support_requests=results, search_query=q)


@main_bp.route("/requests/new", methods=["GET", "POST"])
@login_required
def request_new():
    agents = User.query.filter(User.role.in_(["admin", "agent"]), User.active.is_(True)).all()
    if request.method == "POST":
        support_request = create_support_request(request.form, current_user)
        # Bewuste usabilitybeperking: geen flash/succesmelding.
        return redirect(url_for("main.requests_list"))
    return render_template("request_form.html", agents=agents)


@main_bp.route("/requests/<int:request_id>")
@login_required
def request_detail(request_id):
    support_request = SupportRequest.query.get_or_404(request_id)
    current_app.logger.info("Request %s opened by %s", request_id, current_user.email)
    if request_id % 5 == 0:
        sleep(10)
    return render_template("request_detail.html", support_request=support_request)


@main_bp.route("/requests/<int:request_id>/edit", methods=["GET", "POST"])
@login_required
def request_edit(request_id):
    support_request = SupportRequest.query.get_or_404(request_id)
    if not can_edit_request(current_user):
        current_app.logger.warning("Unauthorized edit attempt by %s", getattr(current_user, "email", "anonymous"))
        abort(403)

    agents = User.query.filter(User.role.in_(["admin", "agent"]), User.active.is_(True)).all()
    if request.method == "POST":
        update_support_request(support_request, request.form, current_user)
        # Bewust wel redirect, maar niet altijd duidelijke feedback.
        return redirect(url_for("main.request_detail", request_id=support_request.id))
    return render_template("edit_request.html", support_request=support_request, agents=agents)


@main_bp.route("/users")
@login_required
def users():
    if current_user.role != "admin":
        abort(403)
    users_list = User.query.order_by(User.name).all()
    return render_template("users.html", users=users_list)
