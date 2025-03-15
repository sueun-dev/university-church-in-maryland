# app/exceptions.py
from typing import Optional, Dict, Any
from flask import Flask, jsonify, render_template


class InvalidUsage(Exception):
    """
    Custom exception class for handling invalid usage scenarios.

    Attributes:
        message: Description of the error.
        status_code: HTTP status code for the error.
        payload: Optional extra data to include in the response.
    """

    status_code: int = 400

    def __init__(
        self,
        message: str = "Invalid usage",
        status_code: Optional[int] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception details into a dictionary."""
        rv: Dict[str, Any] = dict(self.payload or {})
        rv["error"] = self.message
        return rv


def register_error_handlers(app: Flask) -> None:
    """Register custom error handlers with the Flask application."""

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error: InvalidUsage):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500
