import logging
import time
from datetime import datetime

import requests
from django.conf import settings
from django.core.cache import cache
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

HEALTH_CACHE_KEY = "health:dependencies"
HEALTH_CACHE_TTL = 5  # seconds — prevents hammering dependencies on high traffic

def _check_db():
    payload = {"status": "unknown", "latency_ms": None}
    start = time.monotonic()
    try:
        # lightweight probe
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
        latency_ms = (time.monotonic() - start) * 1000
        payload.update(status="ok", latency_ms=round(latency_ms, 2))
    except Exception as exc:
        logger.exception("DB health check failed")
        payload.update(status="failed")
    return payload

def _check_users_service():
    payload = {"status": "unknown", "latency_ms": None}
    url = getattr(settings, "USERS_SERVICE_URL", None)
    if not url:
        payload.update(status="not_configured")
        return payload

    start = time.monotonic()
    try:
        resp = requests.get(f"{url.rstrip('/')}/health/", timeout=2)
        latency_ms = (time.monotonic() - start) * 1000
        payload["latency_ms"] = round(latency_ms, 2)
        payload["status"] = "ok" if resp.status_code == 200 else "unhealthy"
    except requests.RequestException:
        logger.exception("Users service health check failed")
        payload["status"] = "unreachable"
    return payload

@api_view(["GET"])
def index(request):
    """
    Application health endpoint.
    - Returns dependency statuses and latencies.
    - Caches dependency checks for a short TTL.
    - Returns 200 if app is healthy, 503 if any critical dependency is down.
    """
    now_iso = datetime.utcnow().isoformat() + "Z"
    data = {"status": "ok", "timestamp": now_iso}

    # Use cached results to avoid hammering dependencies under load
    cached = cache.get(HEALTH_CACHE_KEY)
    if cached:
        deps = cached
    else:
        deps = {}
        deps["database"] = _check_db()
        deps["users_service"] = _check_users_service()
        cache.set(HEALTH_CACHE_KEY, deps, HEALTH_CACHE_TTL)

    data.update({"dependencies": deps})

    # determine overall status: mark as degraded if any critical dep failed
    critical_bad = any(
        deps[k]["status"] not in ("ok", "not_configured")
        for k in ("database",)
    )
    # treat users_service as non-critical/degraded if unreachable; adjust to your needs
    if critical_bad:
        data["status"] = "degraded"
        return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    # return 200 if everything essential is OK
    return Response(data, status=status.HTTP_200_OK)
