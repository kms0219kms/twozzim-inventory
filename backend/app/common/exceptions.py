from typing import Any, Optional


error_code = {
    "400": "BAD_REQUEST",
    "401": "UNAUTHORIZED",
    "403": "FORBIDDEN",
    "404": "NOT_FOUND",
    "405": "METHOD_NOT_ALLOWED",
    "409": "CONFLICT",
    "410": "GONE",
    "422": "UNPROCESSABLE_CONTENT",
    "429": "TOO_MANY_REQUESTS",
    "500": "INTERNAL_SERVER_ERROR",
    "501": "NOT_IMPLEMENTED",
    "503": "SERVICE_UNAVAILABLE",
}


class APIException(Exception):
    def __init__(
        self,
        status: int,
        code: Optional[str],
        message: Optional[str] = None,
        data: Optional[Any] = None,
    ):
        self.code = code
        self.status = status
        self.message = message
        self.data = data

    def __str__(self) -> str:
        return self.message
