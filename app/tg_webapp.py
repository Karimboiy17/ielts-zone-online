"""Telegram WebApp (Mini App) security — validate initData signature.

Only requests that came from the Telegram bot (with a valid WebApp initData)
can access the app. This makes the site private: it only works inside
Telegram as a mini app, not as a public website.
"""
import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl


def validate_init_data(init_data: str, bot_token: str, max_age: int = 86400) -> dict:
    """Validate Telegram WebApp initData. Returns user dict or raises ValueError."""
    if not init_data or not bot_token:
        raise ValueError("Missing initData or bot token")

    # Parse init data into dict, extracting hash
    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = pairs.pop("hash", "")
    if not received_hash:
        raise ValueError("No hash in initData")

    # Build data-check-string: sorted key=value joined by \n
    items = sorted(pairs.items(), key=lambda kv: kv[0])
    data_check_string = "\n".join(f"{k}={v}" for k, v in items)

    # Secret key = HMAC_SHA256(bot_token, "WebAppData")
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    # Expected hash = HMAC_SHA256(secret_key, data_check_string)
    expected_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected_hash, received_hash):
        raise ValueError("Invalid initData signature")

    # Check auth_date freshness
    auth_date = int(pairs.get("auth_date", "0"))
    if time.time() - auth_date > max_age:
        raise ValueError("initData expired")

    # Parse user object
    user = {}
    if "user" in pairs:
        try:
            user = json.loads(pairs["user"])
        except (json.JSONDecodeError, TypeError):
            user = {}
    return user


def init_data_user(init_data: str, bot_token: str) -> dict:
    """Return the Telegram user dict from a valid initData."""
    return validate_init_data(init_data, bot_token)
