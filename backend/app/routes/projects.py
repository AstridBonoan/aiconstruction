"""Project routes - Monday.com boards (demo)."""

from app.routes import api_bp
from app.services.demo_data import get_demo_tenant, get_demo_boards, get_demo_items


@api_bp.route("/projects", methods=["GET"])
def list_projects():
    """List projects - simulated Monday.com boards."""
    tenant = get_demo_tenant()
    boards = get_demo_boards()
    return {
        "tenant": tenant,
        "projects": boards,
        "source": "monday_demo",
    }, 200


@api_bp.route("/projects/<board_id>/items", methods=["GET"])
def list_board_items(board_id):
    """List items for a board - simulated Monday.com items."""
    items = get_demo_items(board_id)
    return {"items": items, "board_id": board_id}, 200
