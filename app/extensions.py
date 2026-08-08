from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

mongo = PyMongo()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri="memory://",
    enabled=False,
)
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
