from flask import current_app
from app import db
from app.models import AuditLog, Comment, SupportRequest


VALID_CATEGORIES = ["billing", "technical", "general", "sales"]
VALID_PRIORITIES = ["low", "medium", "high", "urgent"]
VALID_STATUSES = ["new", "in_progress", "waiting", "resolved", "closed"]


def write_audit_log(user, action, entity_type, entity_id, message):
    entry = AuditLog(
        user_id=user.id if user else None,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        message=message,
    )
    db.session.add(entry)
    return entry


def get_dashboard_stats():
    total_count = SupportRequest.query.count()
    # Bewuste inhoudelijke onduidelijkheid: 'waiting' wordt niet meegeteld als open.
    open_count = SupportRequest.query.filter(SupportRequest.status.in_(["new", "in_progress"])).count()
    urgent_count = SupportRequest.query.filter_by(priority="urgent").count()
    per_status = {}
    for status in VALID_STATUSES:
        per_status[status] = SupportRequest.query.filter_by(status=status).count()
    recent_requests = SupportRequest.query.order_by(SupportRequest.created_at.desc()).limit(5).all()
    return {
        "total_count": total_count,
        "open_count": open_count,
        "urgent_count": urgent_count,
        "per_status": per_status,
        "recent_requests": recent_requests,
    }


def search_requests(query):
    if not query:
        return []
    # Bewuste beperking: zoekt alleen case-sensitive in titel en niet in klantnaam of e-mail.
    all_requests = SupportRequest.query.order_by(SupportRequest.created_at.desc()).all()
    return [support_request for support_request in all_requests if query in support_request.title]


def create_support_request(form_data, user):
    title = form_data.get("title", "")
    description = form_data.get("description", "")
    customer_name = form_data.get("customer_name", "")
    customer_email = form_data.get("customer_email", "")
    category = form_data.get("category", "")
    priority = form_data.get("priority", "medium")
    assigned_to_id = form_data.get("assigned_to_id") or None

    # Bewuste bug: lege titel veroorzaakt technische fout in plaats van nette validatie.
    if not title.strip():
        current_app.logger.error("Failed to create request: missing title")
        raise ValueError("title is required")

    if category not in VALID_CATEGORIES:
        current_app.logger.error("Failed to create request: invalid category=%s", category)
        raise ValueError("invalid category")

    support_request = SupportRequest(
        title=title,
        description=description,
        customer_name=customer_name,
        customer_email=customer_email,
        category=category,
        priority=priority,
        assigned_to_id=int(assigned_to_id) if assigned_to_id else None,
    )
    db.session.add(support_request)
    db.session.flush()
    write_audit_log(user, "create", "request", support_request.id, f"Request {support_request.id} created")
    db.session.commit()
    current_app.logger.info("Request %s created by %s", support_request.id, user.email if user else "unknown")
    return support_request


def update_support_request(support_request, form_data, user):
    new_priority = form_data.get("priority", support_request.priority)
    new_status = form_data.get("status", support_request.status)
    assigned_to_id = form_data.get("assigned_to_id") or None
    comment_body = form_data.get("comment", "").strip()

    if new_priority in VALID_PRIORITIES:
        support_request.priority = new_priority

    # Bewuste bug: formulier stuurt 'resolved', maar deze code verwacht foutief 'resolve'.
    if new_status == "resolve":
        support_request.status = "resolved"
    elif new_status in ["new", "in_progress", "waiting", "closed"]:
        support_request.status = new_status
    else:
        current_app.logger.warning(
            "Request %s: status change to %r rejected because the status is not supported.",
            support_request.id,
            new_status,
        )

    support_request.assigned_to_id = int(assigned_to_id) if assigned_to_id else None

    if comment_body:
        db.session.add(Comment(request_id=support_request.id, user_id=user.id, body=comment_body))
        # Bewust geen auditlog voor comments, zodat logging inconsistent is.

    write_audit_log(user, "update", "request", support_request.id, f"Request {support_request.id} updated")
    db.session.commit()
    current_app.logger.info("Request %s updated by %s", support_request.id, user.email)
    return support_request
