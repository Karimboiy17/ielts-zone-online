import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "ielts-zone-online-secret-2026")
    _mongo_uri = os.getenv("MONGO_URI") or os.getenv("MONGO_URL") or "mongodb://localhost:27017/ielts_zone"
    MONGO_URI = _mongo_uri
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "ielts_zone")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    SITE_URL = os.getenv("SITE_URL", "http://localhost:5000")
    LOCAL_DEV = os.getenv("LOCAL_DEV", "true").lower() == "true"
    # Narx
    TEST_PRICE = int(os.getenv("TEST_PRICE", "50000"))
    # Telegram bot username (redirect)
    TELEGRAM_BOT = "@IELTSZoneOnlineBot"
    TELEGRAM_BOT_URL = "https://t.me/IELTSZoneOnlineBot"

    # Admin Telegram chat ID (for payment notifications)
    ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", os.getenv("ADMIN_TELEGRAM_ID", ""))

    # Admin credentials (dev default)
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@ieltszone.uz")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123456")

    # SMTP (Gmail) for password reset
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASS = os.getenv("SMTP_PASS", "")
