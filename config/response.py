from typing import Any, Dict, Optional


class HTTPResponse:
    def __init__(self, status_code: int, message: str, data: Any = None, error: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        self.message = message
        self.data = data
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status_code": self.status_code,
            "message": self.message,
            "data": self.data,
            "error": self.error
        }


def set_custom_response(status_code: int, message: str, data: Any = None, error: Optional[Dict[str, Any]] = None):
    return HTTPResponse(status_code, message, data, error)