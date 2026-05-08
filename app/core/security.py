import base64
import hashlib
import hmac
import json
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from app.core.config import get_settings

PASSWORD_ITERATIONS = 210_000


def _base64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _base64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_ITERATIONS,
    )
    return (
        f"pbkdf2_sha256${PASSWORD_ITERATIONS}$"
        f"{_base64url_encode(salt)}${_base64url_encode(password_hash)}"
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations, salt, expected_hash = password_hash.split("$")
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    calculated_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        _base64url_decode(salt),
        int(iterations),
    )
    return hmac.compare_digest(_base64url_encode(calculated_hash), expected_hash)


def create_access_token(user_id: int, perfil: str) -> str:
    settings = get_settings()
    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": str(user_id),
        "perfil": perfil,
        "exp": int(expires_at.timestamp()),
    }

    header_part = _base64url_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_part = _base64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signature = hmac.new(
        settings.secret_key.encode("utf-8"),
        f"{header_part}.{payload_part}".encode("ascii"),
        hashlib.sha256,
    ).digest()

    return f"{header_part}.{payload_part}.{_base64url_encode(signature)}"


def decode_access_token(token: str) -> dict[str, Any] | None:
    settings = get_settings()

    try:
        header_part, payload_part, signature_part = token.split(".")
    except ValueError:
        return None

    expected_signature = hmac.new(
        settings.secret_key.encode("utf-8"),
        f"{header_part}.{payload_part}".encode("ascii"),
        hashlib.sha256,
    ).digest()
    if not hmac.compare_digest(_base64url_encode(expected_signature), signature_part):
        return None

    try:
        payload = json.loads(_base64url_decode(payload_part))
    except (json.JSONDecodeError, ValueError):
        return None

    expires_at = payload.get("exp")
    if not isinstance(expires_at, int) or expires_at < int(datetime.now(UTC).timestamp()):
        return None

    return payload
