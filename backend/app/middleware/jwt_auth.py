"""JWT verification middleware for API requests."""

import jwt
from functools import wraps
from flask import request, jsonify, g
from datetime import datetime, timedelta


def create_token(tenant_id: int, secret: str, expires_hours: int = 24) -> str:
    """Create JWT for tenant session."""
    payload = {
        "tenant_id": tenant_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=expires_hours),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(token: str, secret: str) -> dict:
    """Decode and verify JWT."""
    return jwt.decode(token, secret, algorithms=["HS256"])


def require_jwt(f):
    """Decorator: require valid JWT in Authorization header."""

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return jsonify({"error": "missing_authorization"}), 401
        token = auth[7:].strip()
        if not token:
            return jsonify({"error": "missing_token"}), 401
        try:
            from flask import current_app
            payload = decode_token(token, current_app.config["SECRET_KEY"])
            g.tenant_id = payload.get("tenant_id")
            if not g.tenant_id:
                return jsonify({"error": "invalid_token"}), 401
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token_expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid_token"}), 401

    return decorated
