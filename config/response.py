from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class HTTPResponse:
    status_code: int
    message: str
    data: Any = None
    error: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status_code": self.status_code,
            "message": self.message,
            "data": self.data,
            "error": self.error
        }


@dataclass
class HTTPResponses:
    OK: HTTPResponse = field(default_factory=lambda: HTTPResponse(200, "OK"))
    CREATED: HTTPResponse = field(default_factory=lambda: HTTPResponse(201, "Created"))
    ACCEPTED: HTTPResponse = field(default_factory=lambda: HTTPResponse(202, "Accepted"))
    NO_CONTENT: HTTPResponse = field(default_factory=lambda: HTTPResponse(204, "No Content"))
    BAD_REQUEST: HTTPResponse = field(default_factory=lambda: HTTPResponse(400, "Bad Request"))
    UNAUTHORIZED: HTTPResponse = field(default_factory=lambda: HTTPResponse(401, "Unauthorized"))
    FORBIDDEN: HTTPResponse = field(default_factory=lambda: HTTPResponse(403, "Forbidden"))
    NOT_FOUND: HTTPResponse = field(default_factory=lambda: HTTPResponse(404, "Not Found"))
    METHOD_NOT_ALLOWED: HTTPResponse = field(default_factory=lambda: HTTPResponse(405, "Method Not Allowed"))
    CONFLICT: HTTPResponse = field(default_factory=lambda: HTTPResponse(409, "Conflict"))
    INTERNAL_SERVER_ERROR: HTTPResponse = field(default_factory=lambda: HTTPResponse(500, "Internal Server Error"))
    NOT_IMPLEMENTED: HTTPResponse = field(default_factory=lambda: HTTPResponse(501, "Not Implemented"))
    BAD_GATEWAY: HTTPResponse = field(default_factory=lambda: HTTPResponse(502, "Bad Gateway"))
    SERVICE_UNAVAILABLE: HTTPResponse = field(default_factory=lambda: HTTPResponse(503, "Service Unavailable"))


def set_custom_response(status_code: int, message: str, data: Any = None, error: Optional[Dict[str, Any]] = None):
    return HTTPResponse(status_code, message, data, error)
