"""Risk scoring routes."""

from flask import request
from app.routes import api_bp
from app.services.risk_scoring import score_boards, get_all_item_scores


@api_bp.route("/risk/scores", methods=["GET"])
def risk_scores():
    """Risk scores - boards and items."""
    scope = request.args.get("scope", "all")
    if scope == "boards":
        boards = score_boards()
        return {"scores": boards, "scope": "boards"}, 200
    items = get_all_item_scores()
    return {"scores": items, "scope": "items"}, 200
