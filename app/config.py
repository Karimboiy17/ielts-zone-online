import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "ielts-zone-online-secret-2026")
    # Long exam sessions (~1.5h) — CSRF token must not expire mid-test
    WTF_CSRF_TIME_LIMIT = None
    _mongo_uri = os.getenv("MONGO_URI") or os.getenv("MONGO_URL") or "mongodb://localhost:27017/ielts_zone"
    MONGO_URI = _mongo_uri
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "ielts_zone")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    SITE_URL = os.getenv("SITE_URL", "http://localhost:5000")
    LOCAL_DEV = os.getenv("LOCAL_DEV", "true").lower() == "true"
    # Narx
    TEST_PRICE = int(os.getenv("TEST_PRICE", "50000"))
    # Telegram bot username (redirect)
    TELEGRAM_BOT = "@ieltszonemidtestbot"
    TELEGRAM_BOT_URL = "https://t.me/ieltszonemidtestbot"

    # Admin Telegram chat ID (for payment notifications) — can be comma-separated
    ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", os.getenv("ADMIN_TELEGRAM_ID", ""))
    # All admin chat IDs (Karimboy + Fathulloh coordinator)
    ADMIN_CHAT_IDS = [cid.strip() for cid in ADMIN_CHAT_ID.split(",") if cid.strip()]

    # Admin credentials (dev default)
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@ieltszone.uz")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123456")

    # SMTP (Gmail) for password reset
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASS = os.getenv("SMTP_PASS", "")
