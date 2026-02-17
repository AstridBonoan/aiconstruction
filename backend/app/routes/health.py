"""Health check routes."""

from app.routes import api_bp


@api_bp.route("/health", methods=["GET"])
def api_health():
    """API health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}, 200
