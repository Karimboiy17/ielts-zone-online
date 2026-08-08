import re
import secrets
from datetime import datetime, timezone, timedelta
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.extensions import mongo, csrf, limiter
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("30 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        if not email or not password:
            flash("Iltimos, email va parolni kiriting", "error")
            return render_template("auth/login.html", telegram_bot=current_app.config.get("TELEGRAM_BOT", "@IELTSZoneOnlineBot"))

        # Login by email OR username
        user = User.get_by_email(email)
        if not user:
            user = User.get_by_username(email)
        if not user or not user.check_password(password):
            flash("Email/Login yoki parol noto'g'ri", "error")
            return render_template("auth/login.html", telegram_bot=current_app.config.get("TELEGRAM_BOT", "@IELTSZoneOnlineBot"))

        login_user(user, remember=remember)
        flash(f"Xush kelibsiz, {user.name}!", "success")
        next_page = request.args.get("next")
        return redirect(next_page or url_for("main.index"))

    return render_template("auth/login.html", telegram_bot=current_app.config.get("TELEGRAM_BOT", "@IELTSZoneOnlineBot"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        code = request.form.get("code", "").strip()
        
        if len(code) != 6 or not code.isdigit():
            flash("6 xonali kodni kiriting", "error")
            return render_template("auth/register.html")

        # Find code in DB
        doc = mongo.db.verification_codes.find_one({
            "code": code,
            "used": False,
            "expires_at": {"$gt": datetime.now(timezone.utc)},
        })
        if not doc:
            flash("Kod noto'g'ri yoki muddati o'tgan. Botga /start yozib yangi kod oling.", "error")
            return render_template("auth/register.html")

        email = doc.get("email", f"tg_{code}@telegram.local")
        name = doc.get("name", "User")
        
        # Create user
        username = f"user_{code[:4]}"
        base = username
        counter = 1
        while User.get_by_username(username):
            username = f"{base}{counter}"
            counter += 1

        from werkzeug.security import generate_password_hash as gph
        user = User.create(name, email, gph(code), "", username)

        # Mark code used
        mongo.db.verification_codes.update_one({"_id": doc["_id"]}, {"$set": {"used": True}})

        login_user(user)
        flash("✅ Muvaffaqiyatli ro'yxatdan o'tdingiz!", "success")
        return redirect(url_for("auth.forgot_password"))

    # Generate a code and store it (user gets it from Telegram bot)
    code = str(secrets.randbelow(900000) + 100000)
    mongo.db.verification_codes.insert_one({
        "code": code,
        "used": False,
        "created_at": datetime.now(timezone.utc),
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=10),
    })

    return render_template("auth/register.html", dev_code=code if not current_app.config.get("SMTP_USER") else None)


@auth_bp.route("/verify", methods=["POST"])
def verify():
    email = request.form.get("email", "").strip().lower()
    code = request.form.get("code", "").strip()

    doc = mongo.db.verification_codes.find_one({
        "email": email,
        "code": code,
        "expires_at": {"$gt": datetime.now(timezone.utc)},
    })

    if not doc:
        flash("Kod noto'g'ri yoki muddati o'tgan", "error")
        return render_template("auth/verify.html", email=email)

    # Create user (no password - they'll set it via forgot-password)
    name = email.split("@")[0]
    username = name
    base = username
    counter = 1
    while User.get_by_username(username):
        username = f"{base}{counter}"
        counter += 1

    # Create with empty password (user sets it later via forgot-password)
    from werkzeug.security import generate_password_hash as gph
    user = User.create(name, email, gph(secrets.token_hex(16)), "", username)

    # Clean up used code
    mongo.db.verification_codes.delete_many({"email": email})

    login_user(user)
    flash("Muvaffaqiyatli ro'yxatdan o'tdingiz! Endi parol o'rnating.", "success")
    return redirect(url_for("auth.forgot_password"))


@auth_bp.route("/telegram-link")
@limiter.limit("10 per minute")
def telegram_login_link():
    """One-time login via link from Telegram bot."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    token = request.args.get("token", "").strip()
    if not token:
        flash("Noto'g'ri havola. Botdan yangi link oling.", "error")
        return redirect(url_for("auth.login"))

    doc = mongo.db.login_codes.find_one({
        "token": token,
        "used": False,
        "expires_at": {"$gt": datetime.now(timezone.utc)},
    })

    if not doc:
        flash("Havola muddati o'tgan yoki ishlatilgan. Botdan /start yozib yangi link oling.", "error")
        return redirect(url_for("auth.login"))

    # Find user by tg_id
    tg_id = doc.get("tg_id")
    user = User.get_by_telegram_id(tg_id)
    if not user:
        flash("Foydalanuvchi topilmadi.", "error")
        return redirect(url_for("auth.login"))

    # Mark token used
    mongo.db.login_codes.update_one(
        {"_id": doc["_id"]},
        {"$set": {"used": True}}
    )

    login_user(user, remember=True)
    flash(f"Xush kelibsiz, {user.username}! ✅", "success")
    return redirect(url_for("main.index"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Tizimdan chiqdingiz", "info")
    return redirect(url_for("main.index"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = User.get_by_email(email)
        if not user:
            flash("Bu email bilan foydalanuvchi topilmadi", "error")
            return render_template("auth/forgot_password.html")

        # Generate reset token
        token = secrets.token_urlsafe(32)
        mongo.db.password_resets.insert_one({
            "user_id": user.id,
            "email": email,
            "token": token,
            "used": False,
            "created_at": datetime.now(timezone.utc),
            "expires_at": datetime.now(timezone.utc) + timedelta(hours=1),
        })

        reset_url = url_for("auth.reset_password", token=token, _external=True)

        # Try to send via Email
        sent = False
        if email:
            try:
                import smtplib
                from email.mime.text import MIMEText

                smtp_host = current_app.config.get("SMTP_HOST", "smtp.gmail.com")
                smtp_port = current_app.config.get("SMTP_PORT", 587)
                smtp_user = current_app.config.get("SMTP_USER", "")
                smtp_pass = current_app.config.get("SMTP_PASS", "")

                if smtp_user and smtp_pass:
                    msg = MIMEText(f"Parolni tiklash linki:\n{reset_url}\n\nBu link 1 soat amal qiladi.", "plain", "utf-8")
                    msg["Subject"] = "🔐 IELTS ZONE online - Parolni tiklash"
                    msg["From"] = smtp_user
                    msg["To"] = email

                    server = smtplib.SMTP(smtp_host, smtp_port)
                    server.starttls()
                    server.login(smtp_user, smtp_pass)
                    server.sendmail(smtp_user, [email], msg.as_string())
                    server.quit()
                    sent = True
                    flash("✅ Parolni tiklash linki email orqali yuborildi!", "success")
                    return redirect(url_for("auth.login"))
            except Exception:
                pass

        # Try Telegram as fallback
        if not sent:
            tg = user.telegram
            if tg:
                try:
                    bot_token = current_app.config.get("BOT_TOKEN", "")
                    if bot_token:
                        tg_username = tg.replace("@", "").strip()
                        import requests as req
                        msg = f"🔐 Parolni tiklash\n\nKimdir parolni tiklashni so'radi. Agar bu siz bo'lsangiz, linkni bosing:\n{reset_url}\n\nAgar siz bo'lmasangiz, bu xabarni e'tiborsiz qoldiring."
                        req.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                            json={"chat_id": f"@{tg_username}", "text": msg})
                        flash("✅ Parolni tiklash linki Telegram orqali yuborildi!", "success")
                        return redirect(url_for("auth.login"))
                except Exception:
                    pass

        # If no Telegram, show link directly (for testing)
        flash(f"Parolni tiklash linki: {reset_url}", "info")
        return redirect(url_for("auth.login"))

    return render_template("auth/forgot_password.html")


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    doc = mongo.db.password_resets.find_one({
        "token": token,
        "used": False,
        "expires_at": {"$gt": datetime.now(timezone.utc)},
    })
    if not doc:
        flash("Havola muddati o'tgan yoki ishlatilgan. Qaytadan urinib ko'ring.", "error")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if password != confirm:
            flash("Parollar bir-biriga mos emas", "error")
            return render_template("auth/reset_password.html", token=token)

        if len(password) < 6 or not re.search(r"[A-Z]", password) or not re.search(r"[0-9]", password):
            flash("Parol kamida 6 belgi, 1 katta harf va 1 raqam bo'lishi kerak", "error")
            return render_template("auth/reset_password.html", token=token)

        # Update password
        mongo.db.users.update_one(
            {"_id": ObjectId(doc["user_id"])},
            {"$set": {"password": generate_password_hash(password)}}
        )
        # Mark token used
        mongo.db.password_resets.update_one({"_id": doc["_id"]}, {"$set": {"used": True}})
        flash("✅ Parol muvaffaqiyatli tiklandi! Endi kirishingiz mumkin.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", token=token)
