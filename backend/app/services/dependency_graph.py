"""Dependency graph engine.

Builds nodes and edges from Monday.com item structure.
Supports blocking relationships and critical path analysis.
"""

from app.services.demo_data import (
    get_demo_boards,
    get_demo_items,
    get_demo_dependencies,
    get_all_demo_items_flat,
)
from app.services.risk_scoring import score_item


def build_graph() -> dict:
    """Build dependency graph: nodes + edges.

    Nodes: items with id, label, board_id, risk_level.
    Edges: from depends_on -> to (blocking direction).
    """
    items_flat = get_all_demo_items_flat()
    deps = get_demo_dependencies()
    item_map = {i["id"]: i for i in items_flat}
    scores = {s["item_id"]: s for s in (score_item(it) for it in items_flat)}

    nodes = []
    for item in items_flat:
        iid = item["id"]
        sc = scores.get(iid, {})
        nodes.append({
            "id": iid,
            "label": item["name"],
            "board_id": item.get("board_id", ""),
            "board_name": item.get("board_name", ""),
            "status": (item.get("column_values", {}).get("status") or {}).get("label", "New"),
            "risk_score": sc.get("score", 0),
            "risk_level": sc.get("level", "low"),
        })

    edges = []
    for d in deps:
        from_id = d["to"]
        to_id = d["from"]
        if from_id in item_map and to_id in item_map:
            edges.append({
                "from": from_id,
                "to": to_id,
                "type": "blocks",
            })

    return {"nodes": nodes, "edges": edges}


def get_critical_path() -> list:
    """Identify items on critical path (longest dependency chain)."""
    deps = get_demo_dependencies()
    in_degree = {}
    out_edges = {}
    all_ids = set()

    for d in deps:
        fr, to = d["to"], d["from"]
        all_ids.add(fr)
        all_ids.add(to)
        in_degree[to] = in_degree.get(to, 0) + 1
        if fr not in out_edges:
            out_edges[fr] = []
        out_edges[fr].append(to)

    roots = [n for n in all_ids if in_degree.get(n, 0) == 0]
    depth = {}

    def dfs(node, d):
        depth[node] = max(depth.get(node, 0), d)
        for child in out_edges.get(node, []):
            dfs(child, d + 1)

    for r in roots:
        dfs(r, 0)

    max_d = max(depth.values()) if depth else 0
    critical = [n for n, d in depth.items() if d == max_d]
    return critical
