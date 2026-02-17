"""Demo data layer - simulates Monday.com API response structure.

Mimics Monday.com GraphQL board/item structure for presentation.
Production will replace with real Monday OAuth + GraphQL calls.
"""

DEMO_TENANT = {
    "id": "demo-tenant-1",
    "monday_account_id": "demo_account_123",
    "name": "Acme Construction (Demo)",
    "integration_status": "demo",  # demo | connected
}

DEMO_BOARDS = [
    {
        "id": "1234567890",
        "name": "Riverside Tower - Phase 1",
        "board_type": "project",
        "monday_board_id": "1234567890",
        "item_count": 24,
        "columns": [
            {"id": "status", "title": "Status", "type": "color"},
            {"id": "date", "title": "Due Date", "type": "date"},
            {"id": "people", "title": "Owner", "type": "people"},
        ],
    },
    {
        "id": "1234567891",
        "name": "Westside Industrial Complex",
        "board_type": "project",
        "monday_board_id": "1234567891",
        "item_count": 18,
        "columns": [
            {"id": "status", "title": "Status", "type": "color"},
            {"id": "date", "title": "Due Date", "type": "date"},
            {"id": "people", "title": "Owner", "type": "people"},
        ],
    },
    {
        "id": "1234567892",
        "name": "Downtown Medical Center Expansion",
        "board_type": "project",
        "monday_board_id": "1234567892",
        "item_count": 31,
        "columns": [
            {"id": "status", "title": "Status", "type": "color"},
            {"id": "date", "title": "Due Date", "type": "date"},
            {"id": "people", "title": "Owner", "type": "people"},
        ],
    },
]

# Monday.com items format - column_values as key-value
DEMO_ITEMS = {
    "1234567890": [
        {
            "id": "item_1",
            "name": "Foundation - Excavation",
            "column_values": {
                "status": {"label": "Done", "color": "#00c875"},
                "date": "2025-01-15",
                "people": "J. Martinez",
            },
            "created_at": "2024-11-01T09:00:00Z",
        },
        {
            "id": "item_2",
            "name": "Foundation - Concrete Pour",
            "column_values": {
                "status": {"label": "Done", "color": "#00c875"},
                "date": "2025-01-22",
                "people": "J. Martinez",
            },
            "created_at": "2024-11-01T09:00:00Z",
        },
        {
            "id": "item_3",
            "name": "Structural Steel - Level 1-5",
            "column_values": {
                "status": {"label": "Working on it", "color": "#fdab3d"},
                "date": "2025-02-28",
                "people": "R. Chen",
            },
            "created_at": "2024-11-01T09:00:00Z",
        },
        {
            "id": "item_4",
            "name": "MEP Rough-in - Floors 1-3",
            "column_values": {
                "status": {"label": "Working on it", "color": "#fdab3d"},
                "date": "2025-03-15",
                "people": "S. Patel",
            },
            "created_at": "2024-11-01T09:00:00Z",
        },
        {
            "id": "item_5",
            "name": "Curtain Wall Installation",
            "column_values": {
                "status": {"label": "Stuck", "color": "#e44258"},
                "date": "2025-03-01",
                "people": "M. Johnson",
            },
            "created_at": "2024-11-01T09:00:00Z",
        },
        {
            "id": "item_6",
            "name": "Elevator Shaft Completion",
            "column_values": {
                "status": {"label": "Working on it", "color": "#fdab3d"},
                "date": "2025-03-20",
                "people": "R. Chen",
            },
            "created_at": "2024-11-01T09:00:00Z",
        },
    ],
    "1234567891": [
        {
            "id": "item_7",
            "name": "Site Preparation",
            "column_values": {
                "status": {"label": "Done", "color": "#00c875"},
                "date": "2024-12-01",
                "people": "T. Williams",
            },
            "created_at": "2024-10-15T09:00:00Z",
        },
        {
            "id": "item_8",
            "name": "Warehouse Shell - Steel Frame",
            "column_values": {
                "status": {"label": "Working on it", "color": "#fdab3d"},
                "date": "2025-02-15",
                "people": "T. Williams",
            },
            "created_at": "2024-10-15T09:00:00Z",
        },
        {
            "id": "item_9",
            "name": "Warehouse - Cladding",
            "column_values": {
                "status": {"label": "New", "color": "#c4c4c4"},
                "date": "2025-04-01",
                "people": "M. Johnson",
            },
            "created_at": "2024-10-15T09:00:00Z",
        },
    ],
    "1234567892": [
        {
            "id": "item_10",
            "name": "Demolition - Wing B",
            "column_values": {
                "status": {"label": "Done", "color": "#00c875"},
                "date": "2025-01-10",
                "people": "S. Patel",
            },
            "created_at": "2024-12-01T09:00:00Z",
        },
        {
            "id": "item_11",
            "name": "New HVAC Ductwork",
            "column_values": {
                "status": {"label": "Stuck", "color": "#e44258"},
                "date": "2025-02-20",
                "people": "S. Patel",
            },
            "created_at": "2024-12-01T09:00:00Z",
        },
        {
            "id": "item_12",
            "name": "OR Suite - Electrical",
            "column_values": {
                "status": {"label": "Working on it", "color": "#fdab3d"},
                "date": "2025-03-25",
                "people": "R. Chen",
            },
            "created_at": "2024-12-01T09:00:00Z",
        },
    ],
}

# Dependencies: item_id -> [depends_on_item_ids]
DEMO_DEPENDENCIES = [
    {"from": "item_3", "to": "item_2"},
    {"from": "item_4", "to": "item_3"},
    {"from": "item_5", "to": "item_3"},
    {"from": "item_6", "to": "item_3"},
    {"from": "item_8", "to": "item_7"},
    {"from": "item_9", "to": "item_8"},
    {"from": "item_11", "to": "item_10"},
    {"from": "item_12", "to": "item_11"},
]


def get_demo_tenant():
    """Return simulated tenant/workspace."""
    return DEMO_TENANT


def get_demo_boards():
    """Return simulated Monday.com boards."""
    return DEMO_BOARDS


def get_demo_items(board_id: str):
    """Return simulated Monday.com items for a board."""
    return DEMO_ITEMS.get(board_id, [])


def get_demo_dependencies():
    """Return simulated item dependencies."""
    return DEMO_DEPENDENCIES


def get_all_demo_items_flat():
    """Flatten all items for risk/dependency processing."""
    items = []
    for board_id, board_items in DEMO_ITEMS.items():
        board = next((b for b in DEMO_BOARDS if b["id"] == board_id), None)
        board_name = board["name"] if board else "Unknown"
        for item in board_items:
            items.append({**item, "board_id": board_id, "board_name": board_name})
    return items
