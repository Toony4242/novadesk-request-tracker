from flask import Blueprint, Response, jsonify, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST


monitoring_bp = Blueprint("monitoring", __name__)

REQUEST_COUNTER = Counter("novadesk_requests_total", "Total HTTP requests observed by the simple metrics endpoint", ["method", "path"])


@monitoring_bp.before_app_request
def count_request():
    # Bewust zeer eenvoudige metric zonder statuscode of usercontext.
    REQUEST_COUNTER.labels(method=request.method, path=request.path).inc()


@monitoring_bp.route("/health")
def health():
    # Bewuste beperking: controleert niet of de database bereikbaar is.
    return jsonify({"status": "ok", "app": "NovaDesk Request Tracker"})


@monitoring_bp.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
