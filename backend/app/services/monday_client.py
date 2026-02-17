"""Monday.com GraphQL API client."""

import requests
from app.services.token_service import get_access_token

MONDAY_API_URL = "https://api.monday.com/v2"


def _query(tenant_id: int, query: str, variables: dict = None) -> dict:
    token = get_access_token(tenant_id)
    if not token:
        raise ValueError("No access token for tenant")
    resp = requests.post(
        MONDAY_API_URL,
        json={"query": query, "variables": variables or {}},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise ValueError(data["errors"])
    return data.get("data", {})


def fetch_boards(tenant_id: int) -> list:
    """Fetch all boards for tenant."""
    q = """
    query {
        boards(limit: 100) {
            id
            name
            type
        }
    }
    """
    data = _query(tenant_id, q)
    return data.get("boards", [])


def fetch_board_items(tenant_id: int, board_id: str) -> list:
    """Fetch items for a board with status and dates."""
    q = """
    query ($boardId: ID!) {
        boards(ids: [$boardId]) {
            items_page(limit: 500) {
                items {
                    id
                    name
                    column_values {
                        id
                        type
                        text
                        value
                    }
                }
            }
        }
    }
    """
    data = _query(tenant_id, q, {"boardId": board_id})
    boards = data.get("boards", [])
    if not boards:
        return []
    page = boards[0].get("items_page", {})
    return page.get("items", [])


def fetch_board_item_connections(tenant_id: int, board_id: str) -> list:
    """Fetch item connections (blocking) for dependency graph."""
    q = """
    query ($boardId: ID!) {
        boards(ids: [$boardId]) {
            items_page(limit: 500) {
                items {
                    id
                    connect_boards_syncs {
                        item_id
                        connected_item_id
                    }
                }
            }
        }
    }
    """
    data = _query(tenant_id, q, {"boardId": board_id})
    boards = data.get("boards", [])
    if not boards:
        return []
    items = boards[0].get("items_page", {}).get("items", [])
    deps = []
    for item in items:
        for sync in item.get("connect_boards_syncs", []):
            deps.append({
                "from": sync.get("connected_item_id"),
                "to": item["id"],
            })
    return deps
