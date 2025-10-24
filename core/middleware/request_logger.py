import time
import structlog
from django.utils.deprecation import MiddlewareMixin
from utils.app_logger import get_logger

log = get_logger(__name__)

class RequestLoggerMiddleware(MiddlewareMixin):
    """
    Middleware that logs each incoming request and its corresponding response.
    It captures metadata such as HTTP method, path, status code, and execution time.
    The correlation_id is automatically included (bound by the CorrelationIdMiddleware).
    """

    def process_request(self, request):
        # Record start time for duration tracking
        request._start_time = time.monotonic()

        log.info(
            "request_received",
            method=request.method,
            path=request.path,
            remote_addr=self._get_client_ip(request),
        )

    def process_response(self, request, response):
        # Calculate processing duration
        duration_ms = None
        if hasattr(request, "_start_time"):
            duration_ms = round((time.monotonic() - request._start_time) * 1000, 2)

        log.info(
            "response_sent",
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )
        return response

    def process_exception(self, request, exception):
        log.error(
            "request_failed",
            method=getattr(request, "method", None),
            path=getattr(request, "path", None),
            error=str(exception),
        )

    def _get_client_ip(self, request):
        """
        Extract client IP from request headers.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
