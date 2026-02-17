"""Service to store and retrieve encrypted OAuth tokens."""

from flask import current_app
from app.extensions import db
from app.models import OAuthCredential
from app.utils.token_encryption import encrypt_token, decrypt_token


def _secret() -> str:
    return current_app.config["SECRET_KEY"]


def store_access_token(tenant_id: int, access_token: str, scope: str = "", account_id: str = "") -> None:
    """Encrypt and store access token."""
    enc = encrypt_token(access_token, _secret())
    cred = OAuthCredential.query.filter_by(tenant_id=tenant_id).first()
    if cred:
        cred.access_token_enc = enc
        cred.scope = scope
        cred.account_id = account_id
    else:
        cred = OAuthCredential(
            tenant_id=tenant_id,
            access_token_enc=enc,
            scope=scope,
            account_id=account_id,
        )
        db.session.add(cred)


def get_access_token(tenant_id: int) -> str | None:
    """Decrypt and return access token for tenant."""
    cred = OAuthCredential.query.filter_by(tenant_id=tenant_id).first()
    if not cred or not cred.access_token_enc:
        return None
    return decrypt_token(cred.access_token_enc, _secret())
