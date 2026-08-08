"""
Telegram bot — /start code, payment flow, profile, status.
"""
import time, uuid, requests, logging, threading
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)
_ACTIVE = True

def _main_menu():
    return {"inline_keyboard": [
        [{"text": "🔑 Ro'yxatdan o'tish kodi", "callback_data": "code"},
         {"text": "💳 To'lov", "callback_data": "pay"}],
        [{"text": "📊 Testlarim", "callback_data": "status"},
         {"text": "👤 Profil", "callback_data": "profile"}],
        [{"text": "❓ Yordam", "callback_data": "help"}],
    ]}

def _api(app, method, data, timeout=10):
    token = app.config.get("BOT_TOKEN", "")
    if not token: return None
    try:
        r = requests.post(f"https://api.telegram.org/bot{token}/{method}", json=data, timeout=timeout)
        return r.json() if r.ok else None
    except: return None

def _send(app, chat_id, text, kb=None):
    p = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if kb: p["reply_markup"] = kb
    _api(app, "sendMessage", p)

def _menu(app, chat_id, text):
    _send(app, chat_id, text, _main_menu())

def start_poller(app):
    t = threading.Thread(target=_loop, args=(app,), daemon=True)
    t.start()
    print("  ✓ Bot poller started")

def stop_poller():
    global _ACTIVE; _ACTIVE = False

def _loop(app):
    global _ACTIVE
    offset = 0
    token = app.config.get("BOT_TOKEN", "")
    if not token:
        logger.warning("BOT_TOKEN not set"); return
    api = f"https://api.telegram.org/bot{token}"
    while _ACTIVE:
        try:
            r = requests.get(f"{api}/getUpdates", params={"offset": offset + 1, "timeout": 30}, timeout=35)
            data = r.json()
            if not data.get("ok"): continue
            for u in data.get("result", []):
                offset = u["update_id"]
                _handle(app, u)
        except requests.Timeout: continue
        except Exception as e:
            logger.error(f"Bot: {e}")
            time.sleep(5)

def _handle(app, update):
    cb = update.get("callback_query")
    if cb:
        _callback(app, cb)
        return
    msg = update.get("message")
    if not msg: return
    text = (msg.get("text") or "").strip()
    chat_id = msg["chat"]["id"]
    tg_id = str(msg["from"]["id"])
    uname = msg["from"].get("username", "")
    fname = msg["from"].get("first_name", "User")

    if text.startswith("/start"):
        import secrets
        from app.extensions import mongo
        code = str(secrets.randbelow(900000) + 100000)
        mongo.db.verification_codes.insert_one({
            "code": code, "used": False,
            "tg_id": tg_id, "tg_username": uname, "tg_name": fname,
            "created_at": datetime.now(timezone.utc),
            "expires_at": datetime.now(timezone.utc) + timedelta(minutes=10),
        })
        _send(app, chat_id,
            f"👋 Assalomu alaykum, {fname}!\n\n"
            f"📋 Ro'yxatdan o'tish kodi: <code>{code}</code>\n\n"
            f"1. Saytga o'ting va ro'yxatdan o'ting\n"
            f"2. Kodni kiriting\n"
            f"3. Tayyor!\n\n"
            f"⏳ Kod 10 daqiqa amal qiladi.",
            _main_menu())
        return

    if msg.get("photo"):
        _handle_payment_receipt(app, chat_id, tg_id, fname, msg)
        return

    # Handle text — payment code or test ID
    from app.extensions import mongo
    state = mongo.db.bot_states.find_one({"tg_id": tg_id})
    
    if state and state.get("state") == "awaiting_test_id":
        # User sent a payment code or test ID
        from bson.objectid import ObjectId
        user_input = text.strip()
        attempt = None
        
        # Try as payment code (6-digit number)
        if user_input.isdigit() and len(user_input) == 6:
            attempt = mongo.db.attempts.find_one({"payment_code": user_input})
        
        # Try as ObjectId
        if not attempt:
            try:
                attempt = mongo.db.attempts.find_one({"_id": ObjectId(user_input)})
            except:
                pass
        
        if not attempt:
            _send(app, chat_id, "❌ To'lov kodi topilmadi. Saytdagi 6 xonali kodni yozib yuboring.")
            return
        test = mongo.db.tests.find_one({"_id": attempt.get("test_id")})
        title = test["title"] if test else attempt.get("section", "?")
        price = test["price"] if test else 0
        
        # Save context
        mongo.db.payment_context.update_one(
            {"tg_id": tg_id},
            {"$set": {"attempt_id": str(attempt["_id"]), "test_title": title, "price": price, "updated_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        mongo.db.bot_states.update_one({"tg_id": tg_id}, {"$set": {"state": "awaiting_receipt"}})
        
        _send(app, chat_id,
            f"💳 <b>{title}</b>\n\n"
            f"To'lov summasi: <b>{price} so'm</b>\n\n"
            f"📌 Quyidagi karta/ hisob raqamiga pul o'tkazing:\n"
            f"💳 8600 1234 5678 9012\n"
            f"🏦 Alisher aka\n\n"
            f"To'lovni amalga oshirgach, <b>chek rasmini</b> shu botga yuboring.\n\n"
            f"✅ Admin tasdiqlagach test ochiladi.")
        return

    # Any other text → menu

def _callback(app, cb):
    data = cb.get("data", "")
    chat_id = cb["message"]["chat"]["id"]
    cid = cb["id"]
    _api(app, "answerCallbackQuery", {"callback_query_id": cid})

    if data == "code":
        _send(app, chat_id,
            "🔑 Yangi kod uchun /start yozing.\n\n"
            "Keyin saytda ro'yxatdan o'ting.")
    elif data == "pay":
        tg_id = str(cb.get("from", {}).get("id", ""))
        from app.extensions import mongo
        mongo.db.bot_states.update_one(
            {"tg_id": tg_id},
            {"$set": {"state": "awaiting_test_id", "updated_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        _send(app, chat_id,
            "💰 To'lov qilish\n\n"
            "Saytdagi <b>6 xonali to'lov kodi</b> ni yozib yuboring.\n\n"
            "Misol: <code>473829</code>")
        return
    elif data == "status":
        from app.extensions import mongo
        tg_id = str(cb.get("from", {}).get("id", ""))
        tg_uname = cb.get("from", {}).get("username", "")
        user = mongo.db.users.find_one({"$or": [
            {"telegram": f"@{tg_uname}" if tg_uname else ""},
            {"telegram_id": tg_id},
        ]})
        if not user:
            _send(app, chat_id, "❌ Profil topilmadi.")
            return
        attempts = list(mongo.db.attempts.find({"user_id": user["_id"]}).sort("started_at", -1).limit(10))
        if not attempts:
            _send(app, chat_id, "📭 Hali test ishlamagansiz")
            return
        text = "📊 Testlaringiz:\n\n"
        for a in attempts:
            test = mongo.db.tests.find_one({"_id": a.get("test_id")})
            title = test["title"] if test else a.get("section", "?")
            st = a.get("status", "?")
            pay = a.get("payment_status", "unpaid")
            sc = a.get("score")
            pay_icon = "✅" if pay == "paid" else "⏳" if pay == "checking" else "❌"
            status_icon = "✅" if st == "completed" else "⏳"
            text += f"{pay_icon} {status_icon} {title}"
            if sc is not None: text += f" - {sc}%"
            text += "\n"
        _send(app, chat_id, text)

    elif data == "profile":
        tg_uname = cb.get("from", {}).get("username", "")
        tg_id = str(cb.get("from", {}).get("id", ""))
        _send(app, chat_id,
            f"👤 Telegram: @{tg_uname if tg_uname else 'no username'}\n"
            f"🆔 ID: {tg_id}\n\n"
            f"🌐 Sayt: cefr-platform-app-production.up.railway.app")

    elif data == "help":
        _send(app, chat_id,
            "❓ Yordam\n\n"
            "🔑 /start - ro'yxatdan o'tish kodi\n"
            "💳 To'lov - test uchun to'lov qilish\n"
            "📊 Testlarim - natijalaringiz\n\n"
            "🌐 Sayt: cefr-platform-app-production.up.railway.app")
    else:
        _menu(app, chat_id, "Bosh menyu:")

def _handle_payment_receipt(app, chat_id, tg_id, fname, msg):
    from app.extensions import mongo
    from bson.objectid import ObjectId
    file_id = msg["photo"][-1]["file_id"]
    caption = msg.get("caption", "")

    # Find payment context
    ctx = mongo.db.payment_context.find_one({"tg_id": tg_id})
    attempt_id = ctx["attempt_id"] if ctx else None

    # Store receipt
    receipt = {
        "tg_chat_id": chat_id,
        "tg_id": tg_id,
        "file_id": file_id,
        "attempt_id": attempt_id,
        "caption": caption,
        "created_at": datetime.now(timezone.utc),
        "status": "pending",
    }
    mongo.db.pending_receipts.insert_one(receipt)

    # Notify admin group
    group_id = app.config.get("GROUP_ID", "")
    if group_id and attempt_id:
        try:
            attempt = mongo.db.attempts.find_one({"_id": ObjectId(attempt_id)})
            if attempt:
                user = mongo.db.users.find_one({"_id": attempt.get("user_id")})
                uname = user["username"] if user else "?"
                price = "?"  # Get from test
                _api(app, "sendPhoto", {
                    "chat_id": group_id,
                    "photo": file_id,
                    "caption": f"💳 Yangi to'lov\n👤 {uname}\n🎫 {attempt_id}\n💰 {price} so'm",
                })
        except: pass

    _send(app, chat_id,
        "✅ Chekingiz qabul qilindi! Admin tekshirib, testni faollashtiradi.\n\n"
        "Odatda 10-30 daqiqa ichida tasdiqlanadi.")
