"""Risk scoring engine v1 - rule-based heuristics.

Uses schedule pressure, status, and dependency depth.
ML models will replace this after sufficient production data.
"""

from app.services.demo_data import (
    get_demo_boards,
    get_demo_items,
    get_demo_dependencies,
    get_all_demo_items_flat,
)
from datetime import datetime, date


def _parse_date(val):
    if not val:
        return None
    if isinstance(val, date):
        return val
    try:
        return datetime.strptime(str(val)[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _status_weight(status_label: str) -> float:
    """Higher = more risk."""
    m = {"Stuck": 0.9, "Working on it": 0.5, "Done": 0.0, "New": 0.2}
    return m.get(status_label, 0.3)


def _days_overdue(due_date) -> float:
    if not due_date:
        return 0.0
    d = _parse_date(due_date)
    if not d:
        return 0.0
    today = date.today()
    if d < today:
        return min(1.0, (today - d).days / 30)
    return 0.0


def _schedule_pressure(due_date) -> float:
    """Pressure when due soon."""
    if not due_date:
        return 0.2
    d = _parse_date(due_date)
    if not d:
        return 0.2
    today = date.today()
    delta = (d - today).days
    if delta < 0:
        return 0.9
    if delta <= 7:
        return 0.7
    if delta <= 14:
        return 0.4
    return 0.1


def _build_dependency_depth_map():
    deps = get_demo_dependencies()
    depth = {}
    for d in deps:
        depth[d["from"]] = depth.get(d["to"], 0) + 1
    max_d = max(depth.values()) if depth else 1
    return {k: v / max_d for k, v in depth.items()}


def score_item(item: dict) -> dict:
    """Compute risk score for a single item."""
    cv = item.get("column_values", {})
    status_obj = cv.get("status") or {}
    status_label = status_obj.get("label", "New") if isinstance(status_obj, dict) else str(status_obj)
    due_date = cv.get("date")

    status_r = _status_weight(status_label)
    overdue_r = _days_overdue(due_date)
    pressure_r = _schedule_pressure(due_date)

    depths = _build_dependency_depth_map()
    dep_r = depths.get(item.get("id", ""), 0) * 0.3

    raw = (status_r * 0.35 + overdue_r * 0.3 + pressure_r * 0.2 + dep_r) * 100
    score = min(100, max(0, raw))

    if score >= 75:
        level = "critical"
    elif score >= 50:
        level = "high"
    elif score >= 25:
        level = "medium"
    else:
        level = "low"

    return {
        "item_id": item.get("id"),
        "item_name": item.get("name"),
        "board_id": item.get("board_id"),
        "board_name": item.get("board_name", ""),
        "score": round(score, 1),
        "level": level,
        "factors": {
            "status": status_label,
            "status_contribution": round(status_r * 35, 1),
            "overdue_contribution": round(overdue_r * 30, 1),
            "schedule_pressure": round(pressure_r * 20, 1),
        },
    }


def score_boards() -> list:
    """Compute risk scores per board (aggregate of items)."""
    boards = get_demo_boards()
    items_flat = get_all_demo_items_flat()
    item_scores = [score_item(i) for i in items_flat]

    result = []
    for board in boards:
        bid = board["id"]
        board_scores = [s for s in item_scores if s["board_id"] == bid]
        if not board_scores:
            avg = 0
            level = "low"
        else:
            avg = sum(s["score"] for s in board_scores) / len(board_scores)
            if avg >= 75:
                level = "critical"
            elif avg >= 50:
                level = "high"
            elif avg >= 25:
                level = "medium"
            else:
                level = "low"

        high_risk_items = [s for s in board_scores if s["level"] in ("high", "critical")]
        result.append({
            "board_id": bid,
            "board_name": board["name"],
            "score": round(avg, 1),
            "level": level,
            "item_count": len(board_scores),
            "high_risk_count": len(high_risk_items),
            "top_risks": sorted(board_scores, key=lambda x: -x["score"])[:3],
        })
    return result


def get_all_item_scores() -> list:
    """Return risk scores for all items."""
    items = get_all_demo_items_flat()
    return [score_item(i) for i in items]
