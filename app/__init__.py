import json
from flask import Flask
from app.config import Config
from app.extensions import mongo, login_manager, csrf, limiter


def create_app(config_class=Config):
    app = Flask(__name__,
                template_folder="../templates",
                static_folder="../static",
                static_url_path="/static")
    app.config.from_object(config_class)

    # Register custom Jinja filters
    @app.template_filter("from_json")
    def from_json_filter(value):
        return json.loads(value) if isinstance(value, str) else value

    # Init extensions
    mongo.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # Import models (for user_loader)
    from app import models  # noqa

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.tests import tests_bp
    from app.routes.payment import payment_bp
    from app.routes.admin import admin_bp
    from app.routes.profile import profile_bp
    from app.audio import audio_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tests_bp, url_prefix="/tests")
    app.register_blueprint(payment_bp, url_prefix="/payment")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(audio_bp, url_prefix="/audio")

    # Context processors
    @app.context_processor
    def inject_globals():
        return {
            "site_name": "IELTS ZONE online",
            "price": app.config["TEST_PRICE"],
            "telegram_bot": app.config["TELEGRAM_BOT"],
            "telegram_bot_url": app.config["TELEGRAM_BOT_URL"],
        }

    # Register translations
    from app.translations import _register
    _register(app)

    # Seed data
    with app.app_context():
        _seed_data(app)

    # Start Telegram bot poller in background
    from app.bot_poller import start_poller
    start_poller(app)

    return app


def _seed_data(app):
    """Create default admin and test data if they don't exist."""
    from app.models import User, TestModel
    from werkzeug.security import generate_password_hash

    # Create admin user
    admin = User.get_by_email(app.config["ADMIN_EMAIL"])
    if not admin:
        mongo.db.users.insert_one({
            "username": app.config["ADMIN_USERNAME"],
            "email": app.config["ADMIN_EMAIL"],
            "password": generate_password_hash(app.config["ADMIN_PASSWORD"]),
            "telegram": "",
            "role": "admin",
            "created_at": __import__("datetime").datetime.utcnow(),
        })
        print(f"  ✓ Admin user created: {app.config['ADMIN_EMAIL']}")

    # NOTE: Testlar endi _seed_data da yaratilmaydi.
    # Admin panel orqali qo'lda yaratiladi. DEFAULT_TESTS faqat kod ichida namuna.
    print("  ✓ Test seeding skipped — admin panel orqali yarating")

    # Auto-seed B1+ MID test if missing (deployed on Railway)
    try:
        existing = mongo.db.tests.count_documents({"section": "b1plus_mid"})
        if existing == 0:
            from app.seed_b1plus import seed_b1plus_mid
            seed_b1plus_mid(mongo.db)
            print("  ✓ B1+ MID test auto-seeded")
        else:
            print("  ✓ B1+ MID test already exists")
    except Exception as e:
        print(f"  ⚠ Auto-seed skipped: {e}")

