"""Encrypted token storage for OAuth credentials."""

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def _derive_key(secret: str, salt: bytes = b"construction_ai_oauth") -> bytes:
    """Derive a Fernet key from secret."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret.encode("utf-8")))
    return key


def encrypt_token(plaintext: str, secret: str) -> bytes:
    """Encrypt access token for storage."""
    key = _derive_key(secret)
    f = Fernet(key)
    return f.encrypt(plaintext.encode("utf-8"))


def decrypt_token(ciphertext: bytes, secret: str) -> str:
    """Decrypt stored token."""
    key = _derive_key(secret)
    f = Fernet(key)
    return f.decrypt(ciphertext).decode("utf-8")
