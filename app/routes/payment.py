from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from functools import wraps
from app.extensions import mongo
from bson.objectid import ObjectId
from datetime import datetime, timezone
from flask_login import login_required, current_user

payment_bp = Blueprint("payment", __name__)


def get_attempt(attempt_id):
    try:
        return mongo.db.attempts.find_one({"_id": ObjectId(attempt_id)})
    except Exception:
        return None


@payment_bp.route("/pay/<attempt_id>")
@login_required
def pay(attempt_id):
    attempt = get_attempt(attempt_id)

    if not attempt or str(attempt["user_id"]) != str(current_user.id):
        flash("Test topilmadi", "error")
        return redirect(url_for("tests.test_list"))

    # Fetch test for title & price
    from app.models import TestModel
    test = TestModel.get_by_id(attempt["test_id"])

    # Already paid? redirect to test
    if attempt.get("payment_status") == "paid":
        flash("✅ To'lov tasdiqlangan! Testni boshlashingiz mumkin.", "success")
        if attempt.get("section") == "writing":
            return redirect(url_for("tests.take_test", attempt_id=attempt_id))
        return redirect(url_for("tests.take_test", attempt_id=attempt_id))

    telegram_bot = current_app.config.get("TELEGRAM_BOT", "@IELTSZoneOnlineBot")
    telegram_bot_url = current_app.config.get("TELEGRAM_BOT_URL", "https://t.me/IELTSZoneOnlineBot")

    # Ensure payment_code exists (for existing attempts)
    if not attempt.get("payment_code"):
        import random
        while True:
            code = str(random.randint(100000, 999999))
            if not mongo.db.attempts.find_one({"payment_code": code}):
                break
        mongo.db.attempts.update_one(
            {"_id": ObjectId(attempt_id)},
            {"$set": {"payment_code": code}}
        )
        attempt["payment_code"] = code

    return render_template("payment/index.html",
                         attempt=attempt,
                         test=test,
                         attempt_id=attempt_id,
                         payment_status=attempt.get("payment_status", "unpaid"),
                         telegram_bot=telegram_bot,
                         telegram_bot_url=telegram_bot_url,
                         test_title=test.get("title", "Test"))


@payment_bp.route("/pay/<attempt_id>/confirm", methods=["POST"])
@login_required
def confirm_payment(attempt_id):
    attempt = get_attempt(attempt_id)

    if not attempt or str(attempt["user_id"]) != str(current_user.id):
        flash("Test topilmadi", "error")
        return redirect(url_for("tests.test_list"))

    if attempt.get("payment_status") == "paid":
        flash("✅ To'lov allaqachon tasdiqlangan!", "success")
        if attempt.get("section") == "writing":
            return redirect(url_for("tests.take_test", attempt_id=attempt_id))
        return redirect(url_for("tests.take_test", attempt_id=attempt_id))

    # Check promo code
    promo = request.form.get("promo", "").strip().lower()
    valid_promos = {
        "aliergashev": {"used_by": []},
        "cefr2026": {"used_by": []},
        "welcome": {"used_by": []},
        "cefr2026free": {"used_by": []},
    }

    if promo and promo in valid_promos:
        # Check if already used by this user
        already_used = mongo.db.promo_usage.find_one({
            "code": promo, "user_id": str(current_user.id)
        })
        if already_used:
            flash(f"❌ \"{promo}\" promo kodi allaqachon ishlatilgan!", "error")
            return redirect(url_for("payment.pay", attempt_id=attempt_id))

        # Mark attempt as paid
        mongo.db.attempts.update_one(
            {"_id": ObjectId(attempt_id)},
            {"$set": {
                "payment_status": "paid",
                "paid_at": datetime.now(timezone.utc),
                "promo_code": promo,
            }}
        )

        # Record promo usage
        mongo.db.promo_usage.insert_one({
            "code": promo,
            "user_id": str(current_user.id),
            "username": current_user.username,
            "attempt_id": attempt_id,
            "created_at": datetime.now(timezone.utc),
        })

        flash(f"✅ Promo kod qabul qilindi! Test bepul ochildi.", "success")
        if attempt.get("section") == "writing":
            return redirect(url_for("tests.take_test", attempt_id=attempt_id))
        return redirect(url_for("tests.take_test", attempt_id=attempt_id))

    # Mark as checking (no promo or invalid promo)
    mongo.db.attempts.update_one(
        {"_id": ObjectId(attempt_id)},
        {"$set": {
            "payment_status": "checking",
            "paid_at": datetime.now(timezone.utc),
        }}
    )

    flash("✅ To'lov chekingiz qabul qilindi. Admin tasdiqlashini kuting.", "success")
    return redirect(url_for("payment.pay", attempt_id=attempt_id))
