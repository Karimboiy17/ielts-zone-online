from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app.models import TestAttempt, WritingSubmission
from app.extensions import mongo, csrf
from bson.objectid import ObjectId
from datetime import datetime, timezone
from flask import jsonify
import json

admin_bp = Blueprint("admin", __name__)


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Admin huquqi talab qilinadi", "error")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    # Stats
    total_users = mongo.db.users.count_documents({})
    total_attempts = mongo.db.attempts.count_documents({})
    pending_writing = mongo.db.attempts.count_documents({
        "$or": [
            {"section": "writing", "status": "writing_review", "payment_status": "paid"},
            {"section": "mock", "status": "writing_review", "payment_status": "paid"},
        ]
    })
    pending_payments = mongo.db.attempts.count_documents({
        "payment_status": "checking"
    })
    # Revenue: faqat real to'lov (promokod emas, paid_at bor)
    rev_pipeline = [
        {"$match": {
            "payment_status": "paid",
            "paid_at": {"$exists": True, "$ne": None},
            "$or": [{"promo_code": {"$exists": False}}, {"promo_code": None}, {"promo_code": ""}]
        }},
        {"$lookup": {"from": "tests", "localField": "test_id", "foreignField": "_id", "as": "test"}},
        {"$unwind": "$test"},
        {"$group": {"_id": None, "total": {"$sum": "$test.price"}}}
    ]
    rev_result = list(mongo.db.attempts.aggregate(rev_pipeline))
    total_revenue = rev_result[0]["total"] if rev_result else 0

    return render_template("admin/dashboard.html",
                         total_users=total_users,
                         total_attempts=total_attempts,
                         pending_writing=pending_writing,
                         pending_payments=pending_payments,
                         total_revenue=total_revenue)


@admin_bp.route("/writing")
@login_required
@admin_required
def writing_pending():
    # Include both pure writing tests AND mock tests with ungraded writing
    submissions = list(mongo.db.attempts.find({
        "$or": [
            {"section": "writing", "status": "writing_review"},
            {"section": "mock", "status": "writing_review"},
        ]
    }).sort("completed_at", 1))

    # Enrich with user info
    for s in submissions:
        user = mongo.db.users.find_one({"_id": s.get("user_id")})
        s["user_name"] = user["username"] if user else "Noma'lum"
        s["user_email"] = user["email"] if user else ""
        test = mongo.db.tests.find_one({"_id": s.get("test_id")})
        s["test_title"] = test["title"] if test else s.get("section", "?")
    return render_template("admin/writing.html", submissions=submissions)


@admin_bp.route("/writing/grade/<attempt_id>", methods=["POST"])
@login_required
@admin_required
def grade_writing(attempt_id):
    score = request.form.get("score", type=int)
    feedback = request.form.get("feedback", "").strip()

    if score is None or score < 0 or score > 25:
        flash("Noto'g'ri ball (0-25)", "error")
        return redirect(url_for("admin.writing_pending"))

    # Update attempt with score
    answers = TestAttempt.get_by_id(attempt_id).get("answers", [])
    total = sum(a.get("points_possible", 0) for a in answers)
    percentage = round((score / total) * 100) if total > 0 else 0

    TestAttempt.update(attempt_id, {
        "status": "completed",
        "score": percentage,
        "earned_points": score,
        "total_points": total,
        "feedback": feedback,
        "graded_at": datetime.now(timezone.utc),
    })

    flash("✅ Writing tekshirildi va ball qo'yildi", "success")
    return redirect(url_for("admin.writing_pending"))


@admin_bp.route("/payment/pending")
@login_required
@admin_required
def payment_pending():
    pending = list(mongo.db.attempts.find({
        "payment_status": "checking"
    }).sort("paid_at", 1))
    # Enrich with user info & Telegram check link
    group_id = current_app.config.get("GROUP_ID", "")
    for p in pending:
        user = mongo.db.users.find_one({"_id": p.get("user_id")})
        p["user"] = user
        test = mongo.db.tests.find_one({"_id": p.get("test_id")})
        p["test_title"] = test["title"] if test else p.get("section", "?")
        # Build Telegram check link
        msg_id = p.get("check_telegram_msg_id")
        if msg_id and group_id:
            cid = str(group_id)
            if cid.startswith("-100"):
                cid = cid[4:]
            elif cid.startswith("-"):
                cid = cid[1:]
            p["check_link"] = f"https://t.me/c/{cid}/{msg_id}"
    return render_template("admin/payments.html", pending=pending)


@admin_bp.route("/payment/approve/<attempt_id>")
@login_required
@admin_required
def approve_payment(attempt_id):
    attempt = mongo.db.attempts.find_one({"_id": ObjectId(attempt_id)})
    if not attempt:
        flash("Test topilmadi", "error")
        return redirect(url_for("admin.payment_pending"))

    TestAttempt.update(attempt_id, {
        "payment_status": "paid",
    })

    # Notify user via Telegram
    user = mongo.db.users.find_one({"_id": attempt.get("user_id")})
    if user:
        tg = user.get("telegram", "")
        tg_id = user.get("telegram_id", "")
        bot_token = current_app.config.get("BOT_TOKEN", "")
        if tg and bot_token:
            try:
                import requests as req
                req.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": f"@{tg.replace('@','')}", "text": "✅ To'lo'vingiz tasdiqlandi! Endi testni boshlashingiz mumkin."})
            except: pass

    flash("✅ To'lov tasdiqlandi va foydalanuvchiga xabar yuborildi", "success")
    return redirect(url_for("admin.payment_pending"))


@admin_bp.route("/payment/reject/<attempt_id>")
@login_required
@admin_required
def reject_payment(attempt_id):
    TestAttempt.update(attempt_id, {
        "payment_status": "unpaid",
    })
    flash("❌ To'lov rad etildi", "info")
    return redirect(url_for("admin.payment_pending"))


# ===== TEST MANAGEMENT =====

@admin_bp.route("/tests")
@login_required
@admin_required
def test_list():
    from app.models import TestModel
    tests = list(mongo.db.tests.find({}).sort("section", 1))
    return render_template("admin/tests.html", tests=tests)



@admin_bp.route("/tests/new", methods=["GET", "POST"])
@login_required
@admin_required
def test_new():
    if request.method == "POST":
        return _save_test(None)
    return render_template("admin/test_form.html", test=None)


@admin_bp.route("/tests/<test_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def test_edit(test_id):
    test = mongo.db.tests.find_one({"_id": ObjectId(test_id)})
    if not test:
        flash("Test topilmadi", "error")
        return redirect(url_for("admin.test_list"))

    if request.method == "POST":
        return _save_test(test_id)

    return render_template("admin/test_form.html", test=test)


@admin_bp.route("/tests/<test_id>/delete", methods=["POST"])
@login_required
@admin_required
def test_delete(test_id):
    test_id_obj = ObjectId(test_id)
    # Delete the test
    mongo.db.tests.delete_one({"_id": test_id_obj})
    # Clean up all attempts referencing this test
    deleted = mongo.db.attempts.delete_many({"test_id": test_id_obj})
    count = deleted.deleted_count
    flash(f"✅ Test o'chirildi. {count} ta foydalanuvchi testlari ham tozalandi", "success")
    return redirect(url_for("admin.test_list"))


@admin_bp.route("/tests/<test_id>/toggle", methods=["POST"])
@login_required
@admin_required
def test_toggle(test_id):
    test = mongo.db.tests.find_one({"_id": ObjectId(test_id)})
    if test:
        new_active = not test.get("active", True)
        mongo.db.tests.update_one(
            {"_id": ObjectId(test_id)},
            {"$set": {"active": new_active}}
        )
        status = "faollashtirildi" if new_active else "o'chirildi"
        flash(f"✅ Test {status}", "success")
    return redirect(url_for("admin.test_list"))


def _save_test(test_id=None):
    """Create or update a test from form data."""
    questions_json = request.form.get("questions_json", "[]")
    try:
        questions = json.loads(questions_json)
    except json.JSONDecodeError:
        flash("❌ Savollar formati noto'g'ri (JSON)", "error")
        return redirect(url_for("admin.test_list"))

    section = request.form.get("section", "").strip().lower()
    title = request.form.get("title", "").strip()

    data = {
        "section": section,
        "title": title,
        "icon": request.form.get("icon", "📝").strip(),
        "time_limit": int(request.form.get("time_limit", 30)),
        "price": int(request.form.get("price", 0)),
    }

    # Preserve original_price when updating (only set on create)
    if test_id:
        existing_test = mongo.db.tests.find_one({"_id": ObjectId(test_id)})
        orig_price = existing_test.get("original_price", 25000) if existing_test else 25000
        if orig_price == 0:
            orig_price = 25000  # default if overwritten
        data["original_price"] = orig_price
        data["discount_price"] = int(request.form.get("price", 0))
    else:
        data["original_price"] = int(request.form.get("price", 0))
        data["discount_price"] = int(request.form.get("price", 0))
    data["questions"] = questions
    data["active"] = request.form.get("active") == "on"
    data["audio_url"] = request.form.get("audio_url", "").strip()
    data["audio_parts"] = [request.form.get(f"audio_url_part{i}", "").strip() for i in range(1, 7)]

    if not data["section"] or not data["title"]:
        flash("❌ Section va title majburiy", "error")
        return redirect(url_for("admin.test_list"))
    
    # Validate questions
    if not data.get("questions"):
        flash("❌ Kamida 1 ta savol qo'shing", "error")
        return redirect(url_for("admin.test_list"))
    
    for i, q in enumerate(data["questions"]):
        qid = q.get("id", "").strip()
        if not qid:
            flash(f"❌ Savol {i+1}: ID bo'sh bo'lmasligi kerak", "error")
            return redirect(url_for("admin.test_list"))
        qtext = q.get("question", "").strip()
        if not qtext:
            flash(f"❌ Savol {i+1} ('{qid}'): Matn bo'sh", "error")
            return redirect(url_for("admin.test_list"))
        qtype = q.get("type", "multiple")
        if qtype != "writing" and qtype != "multiple_group":
            options = q.get("options", [])
            if len(options) < 2:
                flash(f"❌ Savol {i+1} ('{qid}'): Kamida 2 variant kerak", "error")
                return redirect(url_for("admin.test_list"))
            for oi, opt in enumerate(options):
                if not opt or not opt.strip():
                    flash(f"❌ Savol {i+1} ('{qid}'): Variant {oi+1} bo'sh", "error")
                    return redirect(url_for("admin.test_list"))
    
    if test_id:
        try:
            mongo.db.tests.update_one(
                {"_id": ObjectId(test_id)},
                {"$set": data}
            )
            flash(f"✅ \"{data['title']}\" yangilandi", "success")
        except Exception as e:
            current_app.logger.error(f"Test save error: {e}")
            flash(f"❌ Saqlashda xatolik: {str(e)[:100]}", "error")
            return redirect(url_for("admin.test_list"))
    else:
        # Check if section already exists
        existing = mongo.db.tests.find_one({"section": data["section"]})
        if existing:
            flash(f"❌ \"{data['section']}\" section allaqachon mavjud", "error")
            return redirect(url_for("admin.test_list"))
        data["created_at"] = datetime.now(timezone.utc)
        mongo.db.tests.insert_one(data)
        flash(f"✅ \"{data['title']}\" testi qo'shildi", "success")
    return redirect(url_for("admin.test_list"))


# ===== USER MANAGEMENT =====


@admin_bp.route("/users")
@login_required
@admin_required
def user_list():
    q = request.args.get("q", "").strip()
    query = {}
    if q:
        query = {
            "$or": [
                {"username": {"$regex": q, "$options": "i"}},
                {"email": {"$regex": q, "$options": "i"}},
                {"telegram": {"$regex": q, "$options": "i"}},
            ]
        }
    users = list(mongo.db.users.find(query).sort("created_at", -1).limit(100))
    for u in users:
        u["attempt_count"] = mongo.db.attempts.count_documents({"user_id": u["_id"]})
        u["paid_count"] = mongo.db.attempts.count_documents({
            "user_id": u["_id"], "payment_status": "paid"
        })

    # Stats for dashboard
    total_users = mongo.db.users.count_documents({})
    total_attempts = mongo.db.attempts.count_documents({})
    paid_attempts = mongo.db.attempts.count_documents({"payment_status": "paid"})
    completed_attempts = mongo.db.attempts.count_documents({"status": "completed"})

    # Attempts by section
    section_counts = {}
    for sec in ["reading", "listening", "grammar", "writing", "mock"]:
        section_counts[sec] = mongo.db.attempts.count_documents({"section": sec})

    # Revenue: faqat real to'lov (promokod emas, paid_at bor)
    pipeline = [
        {"$match": {
            "payment_status": "paid",
            "paid_at": {"$exists": True, "$ne": None},
            "$or": [{"promo_code": {"$exists": False}}, {"promo_code": None}, {"promo_code": ""}]
        }},
        {"$lookup": {"from": "tests", "localField": "test_id", "foreignField": "_id", "as": "test"}},
        {"$unwind": "$test"},
        {"$group": {"_id": None, "total": {"$sum": "$test.price"}}}
    ]
    revenue_result = list(mongo.db.attempts.aggregate(pipeline))
    total_revenue = revenue_result[0]["total"] if revenue_result else 0

    # Users this week
    from datetime import datetime, timedelta, timezone
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    new_users_week = mongo.db.users.count_documents({"created_at": {"$gte": week_ago}})
    attempts_week = mongo.db.attempts.count_documents({"started_at": {"$gte": week_ago}})

    stats = {
        "total_users": total_users,
        "total_attempts": total_attempts,
        "paid_attempts": paid_attempts,
        "completed_attempts": completed_attempts,
        "section_counts": section_counts,
        "total_revenue": total_revenue,
        "new_users_week": new_users_week,
        "attempts_week": attempts_week,
    }

    return render_template("admin/users.html", users=users, q=q, stats=stats)


@admin_bp.route("/users/<user_id>/delete", methods=["POST"])
@login_required
@admin_required
def user_delete(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        flash("Foydalanuvchi topilmadi", "error")
        return redirect(url_for("admin.user_list"))
    if user.get("role") == "admin":
        flash("Adminni o'chirib bo'lmaydi", "error")
        return redirect(url_for("admin.user_list"))
    
    # Delete user's attempts
    mongo.db.attempts.delete_many({"user_id": ObjectId(user_id)})
    # Delete user
    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    flash(f"✅ {user.get('email', '?')} o'chirildi", "success")
    return redirect(url_for("admin.user_list"))


@admin_bp.route("/users/<user_id>")
@login_required
@admin_required
def user_detail(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        flash("Foydalanuvchi topilmadi", "error")
        return redirect(url_for("admin.user_list"))

    attempts = list(mongo.db.attempts.find(
        {"user_id": ObjectId(user_id)}
    ).sort("created_at", -1).limit(50))

    # Enrich with test title
    for a in attempts:
        test = mongo.db.tests.find_one({"_id": a.get("test_id")})
        a["test_name"] = test["title"] if test else a.get("section", "?")
        # CEFR level from score
        score = a.get("score")
        if score is not None:
            from app.cefr import score_to_cefr
            a["cefr"] = score_to_cefr(score)["level"]

    stats = {
        "total_attempts": len(attempts),
        "paid": sum(1 for a in attempts if a.get("payment_status") == "paid"),
        "completed": sum(1 for a in attempts if a.get("status") == "completed"),
        "total_spent": sum(1 for a in attempts if a.get("payment_status") == "paid") * 15000,
    }

    return render_template("admin/user_detail.html",
                         user=user, attempts=attempts, stats=stats)
