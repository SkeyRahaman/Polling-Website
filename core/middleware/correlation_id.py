import uuid
import structlog
from django.utils.deprecation import MiddlewareMixin

class CorrelationIdMiddleware(MiddlewareMixin):
    """
    Middleware that attaches a unique correlation ID to each request.
    If the request includes 'X-Correlation-ID' header, reuse it; otherwise, generate a new UUID4.
    The correlation ID is bound to Structlog context and returned in the response headers.
    """

    def process_request(self, request):
        correlation_id = request.META.get("HTTP_X_CORRELATION_ID", str(uuid.uuid4()))
        request.correlation_id = correlation_id
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)

    def process_response(self, request, response):
        if hasattr(request, "correlation_id"):
            response["X-Correlation-ID"] = request.correlation_id
        return response
