"""Dependency graph routes."""

from app.routes import api_bp
from app.services.dependency_graph import build_graph, get_critical_path


@api_bp.route("/dependencies/graph", methods=["GET"])
def dependency_graph():
    """Dependency graph - nodes and edges."""
    graph = build_graph()
    return graph, 200


@api_bp.route("/dependencies/critical-path", methods=["GET"])
def critical_path():
    """Critical path item IDs."""
    path = get_critical_path()
    return {"critical_path": path}, 200
