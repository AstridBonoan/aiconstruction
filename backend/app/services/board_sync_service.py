"""Board sync engine - syncs Monday.com boards and items to local DB."""

from app.extensions import db
from app.models import Tenant, Board, Item, ItemDependency, OAuthCredential
from app.services.monday_client import fetch_boards, fetch_board_items, fetch_board_item_connections
from app.services.token_service import get_access_token


def sync_tenant_boards(tenant_id: int) -> dict:
    """Sync all boards for a tenant from Monday.com."""
    token = get_access_token(tenant_id)
    if not token:
        return {"synced": 0, "error": "no_token"}

    try:
        monday_boards = fetch_boards(tenant_id)
    except Exception as e:
        return {"synced": 0, "error": str(e)}

    count = 0
    for mb in monday_boards:
        mid = str(mb.get("id", ""))
        name = mb.get("name", "Unnamed")
        btype = mb.get("type", "board")
        board = Board.query.filter_by(tenant_id=tenant_id, monday_board_id=mid).first()
        if board:
            board.name = name
            board.board_type = btype
        else:
            board = Board(tenant_id=tenant_id, monday_board_id=mid, name=name, board_type=btype)
            db.session.add(board)
        db.session.flush()
        count += 1

    db.session.commit()
    return {"synced": count}


def sync_board_items(tenant_id: int, board_id: int) -> dict:
    """Sync items for a board from Monday.com."""
    board = Board.query.filter_by(id=board_id, tenant_id=tenant_id).first()
    if not board or not board.monday_board_id:
        return {"synced": 0, "error": "board_not_found"}

    try:
        monday_items = fetch_board_items(tenant_id, board.monday_board_id)
    except Exception as e:
        return {"synced": 0, "error": str(e)}

    count = 0
    import json
    for mi in monday_items:
        mid = str(mi.get("id", ""))
        name = mi.get("name", "Unnamed")
        status = "new"
        start_date = None
        due_date = None
        for col in mi.get("column_values", []):
            cid = col.get("id", "")
            if cid == "status":
                status = col.get("text", "new") or "new"
            elif col.get("type") == "date" and col.get("value"):
                try:
                    v = json.loads(col["value"])
                    if isinstance(v, dict) and v.get("date"):
                        due_date = v["date"][:10]
                except (json.JSONDecodeError, TypeError):
                    pass

        item = Item.query.filter_by(board_id=board_id, monday_item_id=mid).first()
        if item:
            item.name = name
            item.status = status
            item.due_date = due_date
        else:
            item = Item(board_id=board_id, monday_item_id=mid, name=name, status=status, start_date=start_date, due_date=due_date)
            db.session.add(item)
        count += 1

    db.session.commit()
    return {"synced": count}


def sync_board_dependencies(tenant_id: int, board_id: int) -> dict:
    """Sync item dependencies from Monday.com connections."""
    board = Board.query.filter_by(id=board_id, tenant_id=tenant_id).first()
    if not board or not board.monday_board_id:
        return {"synced": 0, "error": "board_not_found"}

    try:
        deps = fetch_board_item_connections(tenant_id, board.monday_board_id)
    except Exception as e:
        return {"synced": 0, "error": str(e)}

    item_ids = {i.monday_item_id: i.id for i in Item.query.filter_by(board_id=board_id).all()}
    count = 0
    for d in deps:
        from_mid = str(d.get("from", ""))
        to_mid = str(d.get("to", ""))
        item_id = item_ids.get(to_mid)
        depends_on_id = item_ids.get(from_mid)
        if item_id and depends_on_id and item_id != depends_on_id:
            existing = ItemDependency.query.filter_by(item_id=item_id, depends_on_item_id=depends_on_id).first()
            if not existing:
                dep = ItemDependency(item_id=item_id, depends_on_item_id=depends_on_id)
                db.session.add(dep)
                count += 1

    db.session.commit()
    return {"synced": count}
