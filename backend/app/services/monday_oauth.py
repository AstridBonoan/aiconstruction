"""Monday.com OAuth 2.0 service."""

import secrets
import requests
from urllib.parse import urlencode
from flask import current_app


MONDAY_AUTHORIZE_URL = "https://auth.monday.com/oauth2/authorize"
MONDAY_TOKEN_URL = "https://auth.monday.com/oauth2/token"
MONDAY_API_URL = "https://api.monday.com/v2"


def generate_state() -> str:
    """Generate CSRF state parameter."""
    return secrets.token_urlsafe(32)


def get_authorize_url(state: str, subdomain: str = None) -> str:
    """Build Monday.com OAuth authorize URL."""
    params = {
        "client_id": current_app.config["MONDAY_CLIENT_ID"],
        "redirect_uri": current_app.config["MONDAY_OAUTH_REDIRECT_URI"],
        "scope": current_app.config.get("MONDAY_OAUTH_SCOPES", "boards:read boards:write"),
        "state": state,
    }
    if subdomain:
        params["subdomain"] = subdomain
    return f"{MONDAY_AUTHORIZE_URL}?{urlencode(params)}"


def exchange_code_for_token(code: str) -> dict:
    """Exchange authorization code for access token."""
    resp = requests.post(
        MONDAY_TOKEN_URL,
        json={
            "client_id": current_app.config["MONDAY_CLIENT_ID"],
            "client_secret": current_app.config["MONDAY_CLIENT_SECRET"],
            "code": code,
            "redirect_uri": current_app.config["MONDAY_OAUTH_REDIRECT_URI"],
        },
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def get_account_info(access_token: str) -> dict:
    """Fetch Monday account info using access token."""
    query = "{ me { id name email account { id name } } }"
    resp = requests.post(
        MONDAY_API_URL,
        json={"query": query},
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise ValueError(data["errors"])
    return data.get("data", {}).get("me", {})
