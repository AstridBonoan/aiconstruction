"""Monday.com webhook handlers."""

from flask import request, jsonify
from app.routes import api_bp
from app.extensions import db
from app.models import OAuthCredential


def _verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify Monday webhook signature."""
    import hmac
    import hashlib
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature or "")


@api_bp.route("/webhooks/monday", methods=["POST"])
def monday_webhook():
    """Receive Monday.com webhook events for board/item changes."""
    payload = request.get_data()
    signature = request.headers.get("X-Monday-Signature", "")
    # In production, use webhook signing secret from Monday app config
    secret = request.headers.get("X-Monday-Webhook-Secret") or ""

    # For demo/development, accept without verification
    if secret and not _verify_webhook_signature(payload, signature, secret):
        return jsonify({"error": "invalid_signature"}), 401

    try:
        data = request.get_json() or {}
        event = data.get("event", {})
        event_type = event.get("type")
        if event_type == "create_pulse":
            pass  # New item created
        elif event_type == "update_pulse":
            pass  # Item updated
        elif event_type == "delete_pulse":
            pass  # Item deleted
        elif event_type == "change_column_value":
            pass  # Column value changed
        return jsonify({"received": True}), 200
    except Exception:
        return jsonify({"received": False, "error": "processing_failed"}), 500


@api_bp.route("/webhooks/monday/verify", methods=["GET"])
def monday_webhook_verify():
    """Monday.com verifies webhook subscription - return challenge."""
    challenge = request.args.get("challenge")
    if challenge:
        return challenge, 200, {"Content-Type": "text/plain"}
    return jsonify({"error": "missing_challenge"}), 400
