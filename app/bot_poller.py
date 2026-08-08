"""
Telegram bot — /start code, payment flow, profile, status.
"""
import time, uuid, requests, logging, threading
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)
_ACTIVE = True

# Access codes are NOT hardcoded — they're stored in DB (admin-managed)
# and sent to the admin privately. Students never see them from the bot.

def current_app_access_codes(app):
    """Load access codes from DB (admin-managed). Returns {} if none set."""
    try:
        from app.extensions import mongo
        doc = mongo.db.settings.find_one({"key": "access_codes"})
        if doc and doc.get("codes"):
            return dict(doc["codes"])
    except Exception:
        pass
    return {}


def ensure_access_codes(app):
    """Generate fresh random codes on first run and notify admin privately.
    Codes are stored in DB — students never see them from the bot."""
    try:
        from app.extensions import mongo
        doc = mongo.db.settings.find_one({"key": "access_codes"})
        if doc and doc.get("codes"):
            return doc["codes"]
        import secrets, string
        sections = ["novice_mid", "novice_end", "a1_mid", "a1_end",
                    "a2_mid", "a2_end", "b1_mid", "b1_end",
                    "b1plus_mid", "b1plus_end"]
        alphabet = string.ascii_lowercase + string.digits
        codes = {}
        for s in sections:
            codes["".join(secrets.choice(alphabet) for _ in range(8))] = s
        mongo.db.settings.update_one(
            {"key": "access_codes"},
            {"$set": {"codes": codes, "updated_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        # Notify admin privately with the codes
        admin_chat = app.config.get("ADMIN_CHAT_ID", "")
        token = app.config.get("BOT_TOKEN", "")
        if admin_chat and token:
            lines = ["🔑 <b>YANGI IMTIHON KODLARI</b>\n", "Faqat o'qituvchilarga bering:\n"]
            for code, sec in codes.items():
                test = mongo.db.tests.find_one({"section": sec})
                title = test["title"] if test else sec
                lines.append(f"<code>{code}</code> → <b>{title}</b>")
            import requests
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          json={"chat_id": admin_chat, "text": "\n".join(lines),
                                "parse_mode": "HTML"}, timeout=10)
        print(f"  ✓ Access codes generated ({len(codes)} codes)")
        return codes
    except Exception as e:
        print(f"  ⚠ Access codes error: {e}")
        return {}

def _main_menu(site_url=""):
    return {"inline_keyboard": [
        [{"text": "📝 Imtihonni boshlash", "web_app": {"url": site_url}}],
        [{"text": "🔑 Ro'yxatdan o'tish kodi", "callback_data": "code"},
         {"text": "📊 Testlarim", "callback_data": "status"}],
        [{"text": "👤 Profil", "callback_data": "profile"},
         {"text": "❓ Yordam", "callback_data": "help"}],
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
    site_url = app.config.get("SITE_URL", "")
    _send(app, chat_id, text, _main_menu(site_url))

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
        from app.extensions import mongo
        # Reset registration state, start with asking name
        mongo.db.bot_states.update_one(
            {"tg_id": tg_id},
            {"$set": {"state": "awaiting_name", "updated_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        _send(app, chat_id,
            f"👋 Assalomu alaykum, {fname}!\n\n"
            f"📝 Imtihon topshirish uchun avval ro'yxatdan o'ting.\n\n"
            f"1️⃣ <b>Ism familiyangizni</b> yozing.\n\n"
            f"Masalan: <code>Aziz Karimov</code>")
        return

    if msg.get("photo"):
        _handle_payment_receipt(app, chat_id, tg_id, fname, msg)
        return

    # Handle text — registration state machine
    from app.extensions import mongo
    state = mongo.db.bot_states.find_one({"tg_id": tg_id})
    cur_state = (state or {}).get("state", "")

    # ==== STEP 1: awaiting name ====
    if cur_state == "awaiting_name":
        full_name = text.strip()
        if len(full_name.split()) < 1:
            _send(app, chat_id, "❌ Ismingizni yozing, masalan: <code>Aziz Karimov</code>")
            return
        mongo.db.bot_states.update_one(
            {"tg_id": tg_id},
            {"$set": {"state": "awaiting_teacher", "full_name": full_name, "updated_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        _send(app, chat_id,
            f"✅ <b>{full_name}</b> — saqlandi!\n\n"
            f"2️⃣ Endi <b>o'qituvchingizning ismini</b> yozing.\n\n"
            f"Masalan: <code>Alisher aka</code>")
        return

    # ==== STEP 2: awaiting teacher name ====
    if cur_state == "awaiting_teacher":
        teacher = text.strip()
        mongo.db.bot_states.update_one(
            {"tg_id": tg_id},
            {"$set": {"state": "awaiting_code", "teacher_name": teacher, "updated_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        _send(app, chat_id,
            f"✅ O'qituvchi: <b>{teacher}</b> — saqlandi!\n\n"
            f"3️⃣ Endi <b>o'qituvchingiz bergan kodni</b> yozing.\n\n"
            f"🔑 Kodni o'qituvchingizdan oling — u sizga maxsus kod beradi.")
        return

    # ==== STEP 3: awaiting code ====
    if cur_state == "awaiting_code":
        access_codes = current_app_access_codes(app)
        code_key = text.strip().lower().replace(" ", "")
        if code_key not in access_codes:
            _send(app, chat_id, "❌ Kod noto'g'ri. O'qituvchingizdan to'g'ri kodni so'rang.")
            return
        section = access_codes[code_key]
        test = mongo.db.tests.find_one({"section": section, "active": True})
        if not test:
            _send(app, chat_id, "❌ Bu kod uchun test topilmadi. O'qituvchingizga murojaat qiling.")
            return
        title = test.get("title", section)

        # ==== ANTI-DOUBLE-TAKE: check if student already took this test ====
        already = _student_already_took(app, tg_id, section)
        if already:
            _send(app, chat_id,
                f"⚠️ <b>{title}</b> imtihonini siz <b>allaqachon topshirgansiz</b>!\n\n"
                f"📅 Sana: {already.get('completed_at', '—')}\n"
                f"🎯 Ball: {already.get('score', '—')}%\n"
                f"🏆 Daraja: {already.get('cefr_level', '—')}\n\n"
                f"Har bir imtihon faqat <b>bir marta</b> topshiriladi. "
                f"Keyingi darajaga o'tish uchun o'qituvchingizdan yangi kod oling.")
            return

        site_url = app.config.get("SITE_URL", "")
        full_name = (state or {}).get("full_name", fname)
        teacher_name = (state or {}).get("teacher_name", "")
        # Save full registration
        mongo.db.access_grants.update_one(
            {"tg_id": tg_id},
            {"$set": {"code": code_key, "section": section, "test_title": title,
                      "tg_username": uname, "tg_name": full_name,
                      "teacher_name": teacher_name,
                      "granted_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        # Also save to user profile in DB
        _save_student_profile(app, tg_id, full_name, teacher_name, code_key, section)
        # Clear state
        mongo.db.bot_states.update_one({"tg_id": tg_id}, {"$set": {"state": "done"}})
        _send(app, chat_id,
            f"✅ <b>{full_name}</b>, ro'yxatdan o'tdingiz!\n\n"
            f"📚 O'qituvchi: {teacher_name}\n"
            f"📝 Imtihon: <b>{title}</b>\n\n"
            f"👇 Quyidagi tugmani bosing — imtihon Telegram ichida ochiladi.\n\n"
            f"⏱️ Vaqt: {test.get('time_limit', 70)} daqiqa\n"
            f"⚠️ Imtihonni boshlagach, vaqt orqaga qaytmaydi!",
            {"inline_keyboard": [[{"text": f"🚀 {title} imtihonini boshlash",
                                   "web_app": {"url": f"{site_url}/m/{section}/"}}]]})
        return

    # ==== Any other text → menu ====
    _menu(app, chat_id, "Bosh menyu. Ro'yxatdan o'tish uchun <b>/start</b> bosing.")
    return


def _student_already_took(app, tg_id, section):
    """Check if this Telegram user already completed this test section."""
    try:
        from app.extensions import mongo
        # 1) Check completed_tests array on the student doc (authoritative)
        student = mongo.db.students.find_one({"tg_id": str(tg_id)})
        if student and student.get("completed_tests"):
            for t in student["completed_tests"]:
                if t.get("section") == section:
                    return t
        # 2) Fallback: check attempts owned by this user
        user = mongo.db.users.find_one({"telegram_id": str(tg_id)})
        if user:
            attempt = mongo.db.attempts.find_one({
                "user_id": user["_id"],
                "section": section,
                "status": "completed",
            })
            if attempt:
                return attempt
        return None
    except Exception:
        return None


def _save_student_profile(app, tg_id, full_name, teacher_name, code_key, section):
    """Save/update student profile in DB so results can be matched."""
    try:
        from app.extensions import mongo
        mongo.db.students.update_one(
            {"tg_id": tg_id},
            {"$set": {
                "full_name": full_name,
                "teacher_name": teacher_name,
                "code": code_key,
                "section": section,
                "updated_at": datetime.now(timezone.utc),
            }},
            upsert=True,
        )
    except Exception:
        pass

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
