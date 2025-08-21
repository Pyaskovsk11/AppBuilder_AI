"""Minimal offline stub of the :mod:`requests` package.

This stub emulates a tiny subset of the public API that is used inside the
project.  It allows running tests in environments where the real
``requests`` package (and network access) are not available.
"""


class RequestException(Exception):
    """Base exception for all request errors."""


class HTTPError(RequestException):
    """Raised when an HTTP request returns an unsuccessful status code."""


class Response:
    def __init__(self, status_code: int = 200, data: dict | None = None, text: str | None = None):
        self.status_code = status_code
        self._data = data or {}
        self.text = text or str(self._data)

    def json(self) -> dict:
        return self._data

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise HTTPError(f"HTTP {self.status_code}")


def _mock_response(data: dict | None = None, status_code: int = 200) -> Response:
    """Return a :class:`Response` with default data."""
    return Response(status_code, data or {"url": "https://example.com/"})


def post(url, json=None, headers=None, **kwargs) -> Response:  # noqa: D401
    """Simulate ``requests.post`` and return a mock :class:`Response`."""
    return _mock_response()


def patch(url, json=None, headers=None, **kwargs) -> Response:  # noqa: D401
    """Simulate ``requests.patch`` and return a mock :class:`Response`."""
    return _mock_response()


def get(url, params=None, headers=None, **kwargs) -> Response:  # noqa: D401
    """Simulate ``requests.get`` and return a mock :class:`Response`."""
    return _mock_response()


class exceptions:  # pragma: no cover - structure mimics ``requests.exceptions``
    RequestException = RequestException
    HTTPError = HTTPError

