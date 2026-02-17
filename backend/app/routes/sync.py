"""Board sync API routes."""

from flask import request
from app.routes import api_bp
from app.middleware.jwt_auth import require_jwt
from app.services.board_sync_service import sync_tenant_boards, sync_board_items, sync_board_dependencies


@api_bp.route("/sync/boards", methods=["POST"])
@require_jwt
def sync_boards():
    """Sync all boards for the authenticated tenant."""
    from flask import g
    result = sync_tenant_boards(g.tenant_id)
    return result, 200


@api_bp.route("/sync/boards/<int:board_id>/items", methods=["POST"])
@require_jwt
def sync_board_items_route(board_id):
    """Sync items for a board."""
    from flask import g
    result = sync_board_items(g.tenant_id, board_id)
    return result, 200


@api_bp.route("/sync/boards/<int:board_id>/dependencies", methods=["POST"])
@require_jwt
def sync_board_deps_route(board_id):
    """Sync dependencies for a board."""
    from flask import g
    result = sync_board_dependencies(g.tenant_id, board_id)
    return result, 200
