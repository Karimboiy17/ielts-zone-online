"""
Google Sheets + Telegram data manager for IELTS ZONE online platform.

Architecture:
- MongoDB is the SOLE SOURCE OF TRUTH for tests and questions
- Google Sheets stores only: payment records (with Telegram msg ID) and user registrations
- Telegram group stores payment receipt messages (checks)
- Sheet rows reference Telegram message IDs so admins can look up checks
"""

import json
import logging
import os
import time
from functools import lru_cache

import requests
import gspread
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

# ── Configuration ──────────────────────────────────────────────────────────

SHEET_ID = os.getenv("GOOGLE_SHEETS_ID", os.getenv("SHEET_ID", ""))
GROUP_ID = os.getenv("GROUP_ID", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
# Support both raw JSON env var and file path
SA_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")  # raw JSON string (Railway)
SA_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT", "/home/karimboy/xarajat-app/backend/service-account.json")  # file path
PAYMENTS_SHEET = os.getenv("PAYMENTS_SHEET_NAME", "payments")
USERS_SHEET = os.getenv("USERS_SHEET_NAME", "users")

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


# ── Google Sheets Client (cached) ──────────────────────────────────────────

@lru_cache(maxsize=1)
def _get_client():
    """Get cached gspread client."""
    try:
        if SA_JSON:
            sa_info = json.loads(SA_JSON)
            creds = Credentials.from_service_account_info(sa_info, scopes=SCOPE)
        else:
            creds = Credentials.from_service_account_file(SA_PATH, scopes=SCOPE)
        return gspread.authorize(creds)
    except Exception as e:
        logger.warning(f"Google Sheets auth failed: {e}")
        return None


def _get_or_create_ws(sheet_name):
    """Get or create a worksheet by name."""
    client = _get_client()
    if not client or not SHEET_ID:
        return None
    try:
        sheet = client.open_by_key(SHEET_ID)
        try:
            return sheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            ws = sheet.add_worksheet(title=sheet_name, rows=100, cols=10)
            logger.info(f"Created new worksheet: {sheet_name}")
            return ws
    except Exception as e:
        logger.warning(f"Cannot open sheet {SHEET_ID}: {e}")
        return None


# ── Ensure worksheets exist with headers ───────────────────────────────────

def _ensure_payments_ws():
    ws = _get_or_create_ws(PAYMENTS_SHEET)
    if ws:
        try:
            rows = ws.get_all_values()
            if len(rows) < 2 or not rows[0][0].strip():
                # Add header row
                ws.append_row(["date", "username", "telegram", "amount", "test_name", "telegram_message_id", "status"])
        except Exception:
            try:
                ws.append_row(["date", "username", "telegram", "amount", "test_name", "telegram_message_id", "status"])
            except Exception:
                pass
    return ws


def _ensure_users_ws():
    ws = _get_or_create_ws(USERS_SHEET)
    if ws:
        try:
            rows = ws.get_all_values()
            if len(rows) < 2 or not rows[0][0].strip():
                ws.append_row(["date", "username", "email", "telegram_id", "telegram_username"])
        except Exception:
            try:
                ws.append_row(["date", "username", "email", "telegram_id", "telegram_username"])
            except Exception:
                pass
    return ws


# ── Telegram helpers ───────────────────────────────────────────────────────

def _send_telegram_message(text, parse_mode="Markdown"):
    """Send a text message to the Telegram group. Returns message_id or None."""
    if not BOT_TOKEN or not GROUP_ID:
        return None
    for attempt in range(2):
        try:
            resp = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": GROUP_ID, "text": text, "parse_mode": parse_mode},
                timeout=10,
            )
            data = resp.json()
            if data.get("ok"):
                return data["result"]["message_id"]
            else:
                logger.warning(f"Telegram send error: {data.get('description', 'unknown')}")
                time.sleep(1)
        except Exception as e:
            logger.warning(f"Telegram request failed: {e}")
            time.sleep(1)
    return None


def _send_telegram_photo(photo_url, caption=""):
    """Send a photo to the Telegram group. Returns message_id or None."""
    if not BOT_TOKEN or not GROUP_ID:
        return None
    for attempt in range(2):
        try:
            resp = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                json={"chat_id": GROUP_ID, "photo": photo_url, "caption": caption, "parse_mode": "Markdown"},
                timeout=15,
            )
            data = resp.json()
            if data.get("ok"):
                return data["result"]["message_id"]
            else:
                logger.warning(f"Telegram photo send error: {data.get('description', 'unknown')}")
                time.sleep(1)
        except Exception as e:
            logger.warning(f"Telegram photo request failed: {e}")
            time.sleep(1)
    return None


def get_message_link(message_id):
    """Get a Telegram message link from the group."""
    if not GROUP_ID or not message_id:
        return None
    # Remove the leading -100 for link format
    chat_id = str(GROUP_ID)
    if chat_id.startswith("-100"):
        chat_id = chat_id[4:]
    elif chat_id.startswith("-"):
        chat_id = chat_id[1:]
    return f"https://t.me/c/{chat_id}/{message_id}"


# ── Payment receipt → Telegram group ──────────────────────────────────────

def send_payment_receipt_to_telegram(username, amount, test_name, payment_id, photo_url=None):
    """
    Send a payment receipt/check to the Telegram group.
    Returns the Telegram message_id of the receipt, or None.
    """
    text = (
        f"💳 *Yangi to'lov cheki*\n\n"
        f"👤 *Foydalanuvchi:* {username}\n"
        f"📝 *Test:* {test_name}\n"
        f"💰 *Summa:* {amount:,.0f} so'm\n"
        f"🆔 *ID:* `{payment_id}`\n"
        f"📅 *Sana:* {time.strftime('%d.%m.%Y %H:%M')}\n"
        f"┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n"
        f"⏳ *Holat:* Tekshirilmoqda"
    )

    if photo_url:
        msg_id = _send_telegram_photo(photo_url, caption=text)
    else:
        msg_id = _send_telegram_message(text)

    return msg_id


def confirm_payment_in_telegram(message_id):
    """
    Update the payment check message in Telegram to show it's confirmed.
    Edits the message to add a ✅ confirmation.
    """
    if not BOT_TOKEN or not GROUP_ID or not message_id:
        return False
    try:
        # Get the original message first
        resp = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getChat",
            json={"chat_id": GROUP_ID},
            timeout=5,
        )
        # We can't edit a caption of a photo via simple API reliably,
        # so we'll send a follow-up message instead
        follow_up = (
            f"✅ *To'lov tasdiqlandi!*\n"
            f"🆔 Chek ID: `{message_id}`\n"
            f"┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n"
            f"Admin tomonidan tasdiqlangan ✅"
        )
        _send_telegram_message(follow_up)
        return True
    except Exception as e:
        logger.warning(f"Telegram confirm edit error: {e}")
        return False


# ── Payment → Google Sheets ───────────────────────────────────────────────

def log_payment_to_sheet(username, telegram, amount, test_name, telegram_message_id, status="checking"):
    """
    Log a payment to the Google Sheet with the Telegram message ID.
    """
    ws = _ensure_payments_ws()
    if not ws:
        return False

    date_str = time.strftime("%d.%m.%Y %H:%M")
    try:
        ws.append_row([
            date_str,
            username,
            telegram or "",
            str(amount),
            test_name,
            str(telegram_message_id or ""),
            status,
        ])
        logger.info(f"Payment logged to sheet: {username} - {amount} so'm (msg: {telegram_message_id})")
        return True
    except Exception as e:
        logger.warning(f"Payment sheet append error: {e}")
        return False


def update_payment_status_in_sheet(telegram_message_id, new_status="paid"):
    """
    Update payment status in the sheet by Telegram message ID.
    """
    ws = _ensure_payments_ws()
    if not ws:
        return False

    try:
        all_rows = ws.get_all_values()
    except Exception as e:
        logger.warning(f"Sheet read for payment update failed: {e}")
        return False

    if len(all_rows) < 2:
        return False

    headers = all_rows[0]
    try:
        msg_col = headers.index("telegram_message_id")
        status_col = headers.index("status")
    except ValueError:
        return False

    for i, row in enumerate(all_rows[1:], start=2):
        if len(row) > msg_col and row[msg_col].strip() == str(telegram_message_id):
            ws.update_cell(i, status_col + 1, new_status)
            logger.info(f"Payment status updated to {new_status} in sheet row {i}")
            return True

    return False


# ── User registration → Google Sheets ──────────────────────────────────────

def log_user_to_sheet(username, email, telegram_id="", telegram_username=""):
    """
    Log a new user registration to the Google Sheet.
    """
    ws = _ensure_users_ws()
    if not ws:
        return False

    date_str = time.strftime("%d.%m.%Y %H:%M")
    try:
        ws.append_row([
            date_str,
            username,
            email or "",
            telegram_id or "",
            telegram_username or "",
        ])
        logger.info(f"User logged to sheet: {username} ({email})")
        return True
    except Exception as e:
        logger.warning(f"User sheet append error: {e}")
        return False


# ── Find check in Telegram ─────────────────────────────────────────────────

def get_check_url(telegram_message_id):
    """
    Get the Telegram message URL for a check by its message_id.
    Returns a link the admin can click to view the check in the group.
    """
    return get_message_link(telegram_message_id)
