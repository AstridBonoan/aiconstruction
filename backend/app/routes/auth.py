"""OAuth and authentication routes."""

import secrets
from flask import request, redirect, jsonify, session, current_app
from app.routes import api_bp
from app.extensions import db
from app.models import Tenant, OAuthCredential
from app.services.monday_oauth import (
    generate_state,
    get_authorize_url,
    exchange_code_for_token,
    get_account_info,
)


def _session_state_key():
    return "monday_oauth_state"


@api_bp.route("/auth/monday/authorize", methods=["GET"])
def monday_authorize():
    """Start Monday.com OAuth flow - redirect to Monday."""
    state = generate_state()
    session[_session_state_key()] = state
    subdomain = request.args.get("subdomain")
    url = get_authorize_url(state, subdomain)
    return redirect(url)


@api_bp.route("/auth/monday/callback", methods=["GET"])
def monday_callback():
    """Handle OAuth callback from Monday.com."""
    code = request.args.get("code")
    state = request.args.get("state")
    error = request.args.get("error")
    error_description = request.args.get("error_description", "")

    if error:
        return jsonify({"error": error, "description": error_description}), 400

    if not code:
        return jsonify({"error": "missing_code"}), 400

    saved_state = session.pop(_session_state_key(), None)
    if not saved_state or state != saved_state:
        return jsonify({"error": "invalid_state"}), 400

    try:
        token_data = exchange_code_for_token(code)
        access_token = token_data.get("access_token")
        scope = token_data.get("scope", "")

        if not access_token:
            return jsonify({"error": "no_access_token"}), 500

        me = get_account_info(access_token)
        account = me.get("account", {})
        account_id = str(account.get("id", ""))
        account_name = account.get("name", "Unknown")

        tenant = Tenant.query.filter_by(monday_account_id=account_id).first()
        if not tenant:
            tenant = Tenant(monday_account_id=account_id, name=account_name)
            db.session.add(tenant)
            db.session.flush()

        cred = OAuthCredential.query.filter_by(tenant_id=tenant.id).first()
        if cred:
            cred.access_token_enc = access_token.encode("utf-8")  # Will encrypt in token-encryption feature
            cred.scope = scope
            cred.account_id = account_id
        else:
            cred = OAuthCredential(
                tenant_id=tenant.id,
                access_token_enc=access_token.encode("utf-8"),
                scope=scope,
                account_id=account_id,
            )
            db.session.add(cred)

        db.session.commit()

        frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:3000")
        return redirect(f"{frontend_url}?connected=1")
    except Exception as e:
        return jsonify({"error": "token_exchange_failed", "message": str(e)}), 500


@api_bp.route("/auth/status", methods=["GET"])
def auth_status():
    """Return whether Monday is connected (demo: always false for demo mode)."""
    return jsonify({"connected": False, "demo": True}), 200
