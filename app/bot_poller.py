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
    Codes are stored in DB — students never see them from the bot.
    Also adds codes for any NEW sections not yet in the stored set."""
    try:
        from app.extensions import mongo
        import secrets, string
        all_sections = ["novice_mid", "novice_end", "a1_mid", "a1_end",
                        "a2_mid", "a2_end", "preintermediate_mid", "preintermediate_end",
                        "b1_mid", "b1_end",
                        "b1plus_mid", "b1plus_end"]
        alphabet = string.ascii_lowercase + string.digits

        doc = mongo.db.settings.find_one({"key": "access_codes"})
        codes = dict(doc.get("codes", {})) if doc and doc.get("codes") else {}

        # Add codes for missing sections
        new_codes = {}
        for s in all_sections:
            if s not in codes.values():
                code = "".join(secrets.choice(alphabet) for _ in range(8))
                while code in codes:
                    code = "".join(secrets.choice(alphabet) for _ in range(8))
                codes[code] = s
                new_codes[code] = s

        if new_codes or not doc:
            mongo.db.settings.update_one(
                {"key": "access_codes"},
                {"$set": {"codes": codes, "updated_at": datetime.now(timezone.utc)}},
                upsert=True,
            )
            # Notify admin privately with the NEW codes only
            admin_chat = app.config.get("ADMIN_CHAT_ID", "")
            token = app.config.get("BOT_TOKEN", "")
            if admin_chat and token and new_codes:
                lines = ["🔑 <b>YANGI IMTIHON KODLARI</b>\n", "Faqat o'qituvchilarga bering:\n"]
                for code, sec in new_codes.items():
                    test = mongo.db.tests.find_one({"section": sec})
                    title = test["title"] if test else sec
                    lines.append(f"<code>{code}</code> → <b>{title}</b>")
                import requests
                for cid in (app.config.get("ADMIN_CHAT_IDS") or [admin_chat]):
                    if not cid:
                        continue
                    try:
                        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                      json={"chat_id": str(cid).strip(), "text": "\n".join(lines),
                                            "parse_mode": "HTML"}, timeout=10)
                    except Exception:
                        pass
            print(f"  ✓ Access codes ready ({len(codes)} codes, {len(new_codes)} new)")
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

def _send_start_button(app, chat_id, tg_id, title, section, site_url, text):
    """Send the 'start test' WebApp button and remember the message id so it can
    be swapped for a retake button the moment the student opens the test."""
    url = f"{site_url}/m/{section}/?tg={tg_id}"
    kb = {"inline_keyboard": [[{"text": f"🚀 {title} imtihonini boshlash",
                                "web_app": {"url": url}}]]}
    resp = _api(app, "sendMessage",
                {"chat_id": chat_id, "text": text, "parse_mode": "HTML",
                 "reply_markup": kb})
    mid = None
    try:
        if resp and resp.get("ok"):
            mid = resp.get("result", {}).get("message_id")
    except Exception:
        pass
    try:
        from app.extensions import mongo
        mongo.db.bot_states.update_one(
            {"tg_id": str(tg_id)},
            {"$set": {"start_msg_id": mid, "start_msg_chat_id": chat_id,
                      "start_section": section, "start_title": title,
                      "updated_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
    except Exception:
        pass

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

    # ==== ADMIN COMMANDS ====
    if text.strip().lower() in ("/results", "natijalar", "/natijalar"):
        if _is_admin(app, tg_id):
            _send_all_results(app, chat_id)
        else:
            _send(app, chat_id, "❌ Bu buyruq faqat adminlar uchun.")
        return

    if msg.get("photo"):
        _handle_payment_receipt(app, chat_id, tg_id, fname, msg)
        return

    # Handle text — registration state machine
    from app.extensions import mongo
    state = mongo.db.bot_states.find_one({"tg_id": tg_id})
    cur_state = (state or {}).get("state", "")

    # ==== RETake REQUEST: student sends reason → forward to admin ====
    if cur_state == "awaiting_retake_reason":
        reason = text.strip()
        if len(reason) < 3:
            _send(app, chat_id, "❌ Izoh juda qisqa. Sababni batafsilroq yozing.")
            return
        retake_section = (state or {}).get("retake_section", "")
        retake_title = (state or {}).get("retake_title", "imtihon")
        full_name = (state or {}).get("full_name", fname)
        teacher_name = (state or {}).get("teacher_name", "")
        _send_retake_request_to_admin(app, tg_id, full_name, uname,
                                      teacher_name, retake_title, retake_section, reason)
        # Reset state
        mongo.db.bot_states.update_one({"tg_id": tg_id}, {"$set": {"state": "done"}})
        _send(app, chat_id,
            f"✅ So'rovingiz <b>adminga yuborildi</b>!\n\n"
            f"📝 Izoh: {reason}\n"
            f"📚 Imtihon: {retake_title}\n\n"
            f"⏳ Admin tasdiqlagach, qayta ishlashingiz mumkin bo'ladi.")
        return

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
            {"$set": {"state": "awaiting_test", "teacher_name": teacher, "updated_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        _send(app, chat_id,
            f"✅ O'qituvchi: <b>{teacher}</b> — saqlandi!\n\n"
            f"3️⃣ Endi <b>qaysi imtihonni topshirmoqchisiz?</b>\n\n"
            f"👇 Quyidagi tugmalardan birini tanlang:",
            _test_selector_kb())
        return

    # ==== STEP 3: awaiting test selection (inline buttons) ====
    if cur_state == "awaiting_test":
        _send(app, chat_id,
            "📋 Iltimos, quyidagi tugmalardan imtihonni tanlang 👇",
            _test_selector_kb())
        return

    # ==== Any other text → menu ====
    _menu(app, chat_id, "Bosh menyu. Ro'yxatdan o'tish uchun <b>/start</b> bosing.")
    return


def _test_selector_kb():
    """Build inline keyboard with all available exams (no codes needed)."""
    from app.extensions import mongo
    exams = [
        ("novice_mid", "🌱 NOVICE · MID"), ("novice_end", "🌱 NOVICE · END"),
        ("a1_mid", "🔰 A1 · MID"), ("a1_end", "🔰 A1 · END"),
        ("a2_mid", "📘 A2 · MID"), ("a2_end", "📘 A2 · END"),
        ("preintermediate_mid", "📙 PRE-INT · MID"), ("preintermediate_end", "📙 PRE-INT · END"),
        ("b1_mid", "📗 B1 · MID"), ("b1_end", "📗 B1 · END"),
        ("b1plus_mid", "📕 B1+ · MID"), ("b1plus_end", "📕 B1+ · END"),
    ]
    # Only show exams that actually exist in DB
    rows = []
    for section, label in exams:
        try:
            test = mongo.db.tests.find_one({"section": section, "active": True})
            if test:
                rows.append([{"text": label, "callback_data": f"pick_test_{section}"}])
        except Exception:
            pass
    return {"inline_keyboard": rows}


def _send_student_approval_request(app, tg_id, full_name, tg_uname, teacher_name,
                                   test_title, section):
    """Ask all admins to approve this student before they start the test."""
    import requests as _req
    admin_chat = app.config.get("ADMIN_CHAT_ID", "")
    token = app.config.get("BOT_TOKEN", "")
    if not admin_chat or not token:
        return
    text = (
        f"🆕 <b>YANGI O'QUVCHI — TASDIQLASH</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Ism familiya:</b> {full_name}\n"
        f"🆔 Telegram ID: {tg_id}\n"
        f"📱 Telegram: @{tg_uname if tg_uname else '—'}\n"
        f"📚 O'qituvchi: {teacher_name or '—'}\n"
        f"📝 Imtihon: <b>{test_title}</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"Bu o'quvchi rostdan ham shu imtihonni topshishi kerakmi?"
    )
    kb = {"inline_keyboard": [[
        {"text": "✅ Tasdiqlash", "callback_data": f"approve_student_{tg_id}_{section}"},
        {"text": "❌ Rad etish", "callback_data": f"reject_student_{tg_id}_{section}"},
    ]]}
    admin_ids = app.config.get("ADMIN_CHAT_IDS") or [admin_chat]
    for cid in admin_ids:
        if not cid:
            continue
        try:
            _req.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": str(cid).strip(), "text": text,
                            "parse_mode": "HTML", "reply_markup": kb},
                      timeout=10)
        except Exception:
            pass


def _is_admin(app, tg_id):
    """Check if a Telegram ID is an admin."""
    admin_chat = app.config.get("ADMIN_CHAT_ID", "")
    admin_ids = app.config.get("ADMIN_CHAT_IDS") or [admin_chat]
    return str(tg_id) in [str(x).strip() for x in admin_ids]


def _send_all_results(app, chat_id):
    """Send a summary of all completed test results to the requester."""
    try:
        from app.extensions import mongo
        attempts = list(mongo.db.attempts.find(
            {"status": "completed"}
        ).sort("completed_at", -1).limit(50))

        if not attempts:
            _send(app, chat_id, "📭 Hali hech kim test topshirmagan.")
            return

        text = "📊 <b>BARCHA NATIJALAR</b>\n━━━━━━━━━━━━━━━━\n"
        for a in attempts:
            user = mongo.db.users.find_one({"_id": a.get("user_id")})
            name = (user or {}).get("name", "?")
            tg = (user or {}).get("telegram_id", "?")
            test = mongo.db.tests.find_one({"_id": a.get("test_id")})
            title = test["title"] if test else a.get("section", "?")
            score = a.get("score", "?")
            level = a.get("cefr_level", "?")
            text += (f"👤 {name} (ID:{tg})\n"
                     f"   📝 {title} | 🎯 {score}% | 🏆 {level}\n")

        # Telegram message limit 4096 — split if needed
        if len(text) > 3900:
            text = text[:3900] + "\n..."
        _send(app, chat_id, text)
    except Exception as e:
        _send(app, chat_id, f"❌ Natijalarni olishda xato: {e}")


def _send_retake_request_to_admin(app, tg_id, full_name, tg_uname, teacher_name,
                                  test_title, section, reason):
    """Forward a retake request to all admin chats with Approve/Reject buttons."""
    import requests as _req
    admin_chat = app.config.get("ADMIN_CHAT_ID", "")
    token = app.config.get("BOT_TOKEN", "")
    if not admin_chat or not token:
        return
    text = (
        f"🔁 <b>QAYTA ISHLASH SO'ROVI</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 <b>O'quvchi:</b> {full_name}\n"
        f"🆔 Telegram ID: {tg_id}\n"
        f"📱 Telegram: @{tg_uname if tg_uname else '—'}\n"
        f"📚 O'qituvchi: {teacher_name or '—'}\n"
        f"📝 Imtihon: <b>{test_title}</b>\n"
        f"🔑 Section: {section}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"💬 <b>Izoh:</b> {reason}"
    )
    kb = {"inline_keyboard": [[
        {"text": "✅ Tasdiqlash", "callback_data": f"retake_approve_{tg_id}_{section}"},
        {"text": "❌ Rad etish", "callback_data": f"retake_reject_{tg_id}_{section}"},
    ]]}
    # Send to all admin chats (comma-separated)
    admin_ids = app.config.get("ADMIN_CHAT_IDS") or [admin_chat]
    for cid in admin_ids:
        if not cid:
            continue
        try:
            _req.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": str(cid).strip(), "text": text,
                            "parse_mode": "HTML", "reply_markup": kb},
                      timeout=10)
        except Exception:
            pass


def _student_already_took(app, tg_id, section):
    """Check if this Telegram user already started/completed this test section.
    ANY started attempt blocks retake — closing the test without finishing
    still locks it (no double-take)."""
    try:
        from app.extensions import mongo
        # 1) Check completed_tests array on the student doc (authoritative)
        student = mongo.db.students.find_one({"tg_id": str(tg_id)})
        if student and student.get("completed_tests"):
            for t in student["completed_tests"]:
                if t.get("section") == section:
                    return t
        # 2) Fallback: check attempts owned by this user (started OR completed)
        user = mongo.db.users.find_one({"telegram_id": str(tg_id)})
        if user:
            attempt = mongo.db.attempts.find_one({
                "user_id": user["_id"],
                "section": section,
                "status": {"$in": ["started", "completed"]},
            })
            if attempt:
                return attempt
        # 3) Direct: attempts carrying tg_id (mini-app start links the student)
        attempt = mongo.db.attempts.find_one({
            "tg_id": str(tg_id),
            "section": section,
            "status": {"$in": ["started", "completed"]},
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

    # Student picks a test from the selector: pick_test_<section>
    if data.startswith("pick_test_"):
        section = data[len("pick_test_"):]
        tg_id = str(cb.get("from", {}).get("id", ""))
        tg_uname = cb.get("from", {}).get("username", "")
        from app.extensions import mongo

        st = mongo.db.bot_states.find_one({"tg_id": tg_id})
        full_name = (st or {}).get("full_name", "O'quvchi")
        teacher_name = (st or {}).get("teacher_name", "")
        test = mongo.db.tests.find_one({"section": section, "active": True})
        if not test:
            _send(app, chat_id, "❌ Bu imtihon hozircha mavjud emas. O'qituvchingizga murojaat qiling.")
            return
        title = test.get("title", section)

        # ==== ANTI-DOUBLE-TAKE ====
        already = _student_already_took(app, tg_id, section)
        if already:
            mongo.db.bot_states.update_one(
                {"tg_id": tg_id},
                {"$set": {"retake_section": section, "retake_title": title,
                          "updated_at": datetime.now(timezone.utc)}},
                upsert=True,
            )
            if already.get("status") == "started" or not already.get("completed_at"):
                msg = (f"⚠️ <b>{title}</b> imtihonini siz <b>allaqachon boshlagansiz</b>!\n\n"
                       f"📅 Boshlangan: {str(already.get('started_at', '—'))[:16]}\n\n"
                       f"Har bir imtihon faqat <b>bir marta</b> boshlanadi.\n"
                       f"Testni tugatmasdan chiqib ketgan bo'lsangiz, qayta ishlash "
                       f"uchun tugmani bosing — so'rovingiz adminga yuboriladi.")
            else:
                msg = (f"⚠️ <b>{title}</b> imtihonini siz <b>allaqachon topshirgansiz</b>!\n\n"
                       f"📅 Sana: {str(already.get('completed_at', '—'))[:16]}\n"
                       f"🎯 Ball: {already.get('score', '—')}%\n"
                       f"🏆 Daraja: {already.get('level', already.get('cefr_level', '—'))}\n\n"
                       f"Har bir imtihon faqat <b>bir marta</b> topshiriladi.\n"
                       f"Qayta ishlash uchun tugmani bosing — so'rovingiz adminga yuboriladi.")
            _send(app, chat_id, msg,
                  {"inline_keyboard": [[{"text": "🔁 Qayta ishlash so'rovi yuborish",
                                         "callback_data": "retake_request"}]]})
            return

        # Save registration
        _save_student_profile(app, tg_id, full_name, teacher_name, "", section)

        # ==== ADMIN APPROVAL GATE ====
        student_doc = mongo.db.students.find_one({"tg_id": tg_id})
        approved_sections = (student_doc or {}).get("approved_sections", [])
        if section in approved_sections:
            # Already approved — open test directly
            site_url = app.config.get("SITE_URL", "")
            mongo.db.bot_states.update_one({"tg_id": tg_id}, {"$set": {"state": "done"}})
            _send_start_button(app, chat_id, tg_id, title, section, site_url,
                f"✅ <b>{full_name}</b>, ro'yxatdan o'tdingiz!\n\n"
                f"📚 O'qituvchi: {teacher_name}\n"
                f"📝 Imtihon: <b>{title}</b>\n\n"
                f"👇 Quyidagi tugmani bosing — imtihon Telegram ichida ochiladi.\n\n"
                f"⏱️ Vaqt: {test.get('time_limit', 70)} daqiqa\n"
                f"⚠️ Imtihonni boshlagach, vaqt orqaga qaytmaydi!")
            return

        # Not approved yet — ask admin
        mongo.db.bot_states.update_one(
            {"tg_id": tg_id},
            {"$set": {"state": "awaiting_approval", "pending_section": section,
                      "pending_title": title, "updated_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        _send_student_approval_request(app, tg_id, full_name, tg_uname,
                                       teacher_name, title, section)
        _send(app, chat_id,
            f"📝 <b>{full_name}</b>, so'rovingiz <b>adminga yuborildi</b>!\n\n"
            f"📚 O'qituvchi: {teacher_name}\n"
            f"📝 Imtihon: <b>{title}</b>\n\n"
            f"⏳ Admin sizni tasdiqlashi kutilmoqda. Tasdiqlangach, imtihon ochiladi.\n"
            f"Buni odatda 1-2 daqiqa ichida qilamiz. Iltimos kuting... 🙏")
        return

    # Admin approves/rejects NEW student approval: approve_student_<tg_id>_<section>
    if data.startswith("approve_student_") or data.startswith("reject_student_"):
        parts = data.split("_")
        # format: approve|reject, student, <tg_id>, <section>
        if len(parts) >= 4:
            action = parts[0]
            student_tg_id = parts[2]
            section = "_".join(parts[3:])
            from app.extensions import mongo

            student = mongo.db.students.find_one({"tg_id": student_tg_id})
            sname = (student or {}).get("full_name", "O'quvchi")
            test_title = mongo.db.tests.find_one({"section": section})
            title = test_title["title"] if test_title else section

            if action == "approve":
                # Mark approved for this section
                mongo.db.students.update_one(
                    {"tg_id": student_tg_id},
                    {"$addToSet": {"approved_sections": section}},
                    upsert=True,
                )
                mongo.db.bot_states.update_one(
                    {"tg_id": student_tg_id},
                    {"$set": {"state": "done", "updated_at": datetime.now(timezone.utc)}},
                    upsert=True,
                )
                site_url = app.config.get("SITE_URL", "")
                # Notify student — give them the test button
                _send_start_button(app, student_tg_id, student_tg_id, title, section, site_url,
                    f"✅ <b>{sname}</b>, siz <b>tasdiqlandingiz</b>!\n\n"
                    f"📝 Imtihon: <b>{title}</b>\n\n"
                    f"👇 Quyidagi tugmani bosing — imtihon Telegram ichida ochiladi.\n\n"
                    f"⏱️ Vaqt: {test_title['time_limit'] if test_title else 70} daqiqa\n"
                    f"⚠️ Imtihonni boshlagach, vaqt orqaga qaytmaydi!")
                # Reply to admin
                _send(app, chat_id, f"✅ <b>{sname}</b> tasdiqlandi — imtihon ochildi!")
            else:
                # Reject — notify student
                mongo.db.bot_states.update_one(
                    {"tg_id": student_tg_id},
                    {"$set": {"state": "rejected", "updated_at": datetime.now(timezone.utc)}},
                    upsert=True,
                )
                _send(app, student_tg_id,
                    f"❌ <b>{sname}</b>, so'rovingiz <b>rad etildi</b>.\n\n"
                    f"Imtihon topshish uchun o'qituvchingizga murojaat qiling.")
                _send(app, chat_id, f"❌ <b>{sname}</b> rad etildi.")
        return

    # Admin approves/rejects retake request: retake_approve_<tg_id>_<section>
    if data.startswith("retake_approve_") or data.startswith("retake_reject_"):
        parts = data.split("_")
        # format: retake, approve|reject, <tg_id>, <section>
        if len(parts) >= 4:
            action = parts[1]
            student_tg_id = parts[2]
            section = "_".join(parts[3:])
            from app.extensions import mongo

            # Find student info
            student = mongo.db.students.find_one({"tg_id": student_tg_id})
            sname = (student or {}).get("full_name", "O'quvchi")
            test_title = mongo.db.tests.find_one({"section": section})
            title = test_title["title"] if test_title else section

            if action == "approve":
                # Allow retake: remove locked attempts + completed record for this section
                user = mongo.db.users.find_one({"telegram_id": student_tg_id})
                if user:
                    mongo.db.attempts.delete_many({
                        "user_id": user["_id"],
                        "section": section,
                    })
                # Also remove attempts linked via tg_id (mini-app start path)
                mongo.db.attempts.delete_many({
                    "tg_id": student_tg_id,
                    "section": section,
                })
                if student and student.get("completed_tests"):
                    mongo.db.students.update_one(
                        {"tg_id": student_tg_id},
                        {"$set": {"completed_tests": [
                            t for t in student["completed_tests"] if t.get("section") != section
                        ]}}
                    )
                if student and student.get("started_tests"):
                    mongo.db.students.update_one(
                        {"tg_id": student_tg_id},
                        {"$set": {"started_tests": [
                            t for t in student["started_tests"] if t.get("section") != section
                        ]}}
                    )
                # Reset bot state so the student can re-register
                mongo.db.bot_states.update_one(
                    {"tg_id": student_tg_id},
                    {"$set": {"state": "done", "retake_approved": True,
                              "retake_section": section, "updated_at": datetime.now(timezone.utc)}},
                    upsert=True,
                )
                # Notify student — give a fresh start button right away
                site_url = app.config.get("SITE_URL", "")
                _send_start_button(app, student_tg_id, student_tg_id, title, section, site_url,
                    f"✅ <b>{title}</b> imtihonini qayta ishlashga <b>ruxsat berildi</b>!\n\n"
                    f"👇 Quyidagi tugmani bosing — imtihon yangidan ochiladi.\n\n"
                    f"⏱️ Vaqt: {test_title['time_limit'] if test_title else 70} daqiqa\n"
                    f"⚠️ Imtihonni boshlagach, vaqt orqaga qaytmaydi!")
                # Reply to admin
                _send(app, chat_id, f"✅ <b>{sname}</b> uchun <b>{title}</b> qayta ishlash tasdiqlandi!")
            else:
                # Notify student rejected
                _send(app, student_tg_id,
                    f"❌ <b>{title}</b> imtihonini qayta ishlash so'rovingiz <b>rad etildi</b>.\n\n"
                    f"Batafsil ma'lumot uchun o'qituvchingizga murojaat qiling.")
                # Reply to admin
                _send(app, chat_id, f"❌ <b>{sname}</b> uchun <b>{title}</b> qayta ishlash rad etildi.")
        return

    if data == "retake_request":
        tg_id = str(cb.get("from", {}).get("id", ""))
        from app.extensions import mongo
        st = mongo.db.bot_states.find_one({"tg_id": tg_id})
        title = (st or {}).get("retake_title", "imtihon")
        mongo.db.bot_states.update_one(
            {"tg_id": tg_id},
            {"$set": {"state": "awaiting_retake_reason", "updated_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        _send(app, chat_id,
            f"🔁 <b>{title}</b> imtihonini qayta ishlash so'rovi.\n\n"
            f"📝 Nega qayta ishlamoqchisiz? <b>Izoh yozing</b> — adminga yuboriladi.\n\n"
            f"Masalan: <i>Internet uzilib qoldi, test tugamadi</i>")
        return

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
