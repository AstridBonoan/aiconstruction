"""Executive dashboard service - aggregates KPIs."""

from app.services.demo_data import get_demo_tenant, get_demo_boards, get_all_demo_items_flat
from app.services.risk_scoring import score_boards, get_all_item_scores


def get_executive_kpis() -> dict:
    """Compute portfolio-level KPIs."""
    tenant = get_demo_tenant()
    boards = get_demo_boards()
    items = get_all_demo_items_flat()
    board_scores = score_boards()
    item_scores = get_all_item_scores()

    total_projects = len(boards)
    total_tasks = len(items)
    done = sum(1 for i in items if (i.get("column_values", {}).get("status") or {}).get("label") == "Done")
    in_progress = sum(1 for i in items if (i.get("column_values", {}).get("status") or {}).get("label") == "Working on it")
    stuck = sum(1 for i in items if (i.get("column_values", {}).get("status") or {}).get("label") == "Stuck")

    avg_risk = sum(s["score"] for s in item_scores) / len(item_scores) if item_scores else 0
    high_risk_count = sum(1 for s in item_scores if s["level"] in ("high", "critical"))
    critical_count = sum(1 for s in item_scores if s["level"] == "critical")

    completion_pct = round(100 * done / total_tasks, 1) if total_tasks else 0

    return {
        "tenant": tenant,
        "kpis": {
            "total_projects": total_projects,
            "total_tasks": total_tasks,
            "tasks_complete": done,
            "tasks_in_progress": in_progress,
            "tasks_stuck": stuck,
            "completion_percent": completion_pct,
            "avg_risk_score": round(avg_risk, 1),
            "high_risk_items": high_risk_count,
            "critical_risk_items": critical_count,
        },
        "boards": board_scores,
    }
