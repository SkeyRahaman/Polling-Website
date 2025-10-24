# connectors/users_client.py
import asyncio
import httpx
from typing import Optional, Any, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from django.conf import settings
from utils.app_logger import get_logger

log = get_logger(__name__)

DEFAULT_TIMEOUT = getattr(settings, "USERS_CLIENT_TIMEOUT", 5.0)
BASE_URL = getattr(settings, "USERS_SERVICE_URL", "http://users.internal.svc")

class UsersClientError(Exception): ...
class UsersNotFound(UsersClientError): ...
class UsersAuthError(UsersClientError): ...

class UsersClient:
    def __init__(self, base_url: str = BASE_URL, timeout: float = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
        self._lock = asyncio.Lock()

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            async with self._lock:
                if self._client is None:
                    self._client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def _headers(self, correlation_id: Optional[str] = None) -> Dict[str, str]:
        h = {"Accept": "application/json"}
        if correlation_id:
            h["X-Correlation-ID"] = correlation_id
        return h

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=0.2, max=2))
    async def check_health(self, correlation_id: Optional[str] = None):
        """Calls the /health endpoint of the users service."""
        headers = {"Accept": "application/json"}
        if correlation_id:
            headers["X-Correlation-ID"] = correlation_id

        try:
            log.info(f"Making a API call to Users Service /health endpoint with url - {self.base_url}/health")
            client = await self._get_client()
            resp = await client.get("/health", headers=headers)
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as e:
            log.error("users_client.network_error", error=str(e))
            raise UsersClientError(f"Network error: {e}")
        except httpx.HTTPStatusError as e:
            log.error("users_client.bad_response", status=e.response.status_code)
            raise UsersClientError(f"HTTP error: {e.response.status_code}")
