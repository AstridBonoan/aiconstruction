"""Dashboard routes - executive portfolio view."""

from app.routes import api_bp
from app.services.dashboard_service import get_executive_kpis


@api_bp.route("/dashboard/kpis", methods=["GET"])
def dashboard_kpis():
    """Executive dashboard KPIs."""
    data = get_executive_kpis()
    return data, 200
