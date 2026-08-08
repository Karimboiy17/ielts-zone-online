"""
Simple translation system for Flask templates.
4 languages: uz (default), en, ru, kaa
Usage in templates: {{ _('hello') }} or {{ _('welcome', name=user) }}
"""
import json
import os
import re

_TRANSLATIONS_DIR = os.path.join(os.path.dirname(__file__), "translations")
_CACHE = {}

LANGUAGES = {
    "uz": "O'zbek",
    "en": "English",
    "ru": "Русский",
    "kaa": "Қарақалпақша",
}
LANGUAGE_FLAGS = {
    "uz": "🇺🇿",
    "en": "🇬🇧",
    "ru": "🇷🇺",
    "kaa": "🏳️",
}


def load_translations(lang):
    """Load translation dict for a language, cached."""
    if lang in _CACHE:
        return _CACHE[lang]
    path = os.path.join(_TRANSLATIONS_DIR, f"{lang}.json")
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    _CACHE[lang] = data
    return data


def t(key, lang="uz", **kwargs):
    """Translate a key to the given language with variable substitution."""
    translations = load_translations(lang)
    # Flat lookup (keys like 'nav.home', 'hero.title')
    val = translations.get(key) if isinstance(translations, dict) else None
    # Fallback: try Uzbek
    if val is None:
        uz = load_translations("uz")
        val = uz.get(key) if isinstance(uz, dict) else None
    if val is None:
        return key  # key not found, return the key itself
    # Substitute {{var}} placeholders
    if kwargs:
        for k, v in kwargs.items():
            val = str(val).replace("{{" + k + "}}", str(v))
    return val


def _register(app):
    """Register the translation filter and context processor with the Flask app."""

    @app.template_filter("t")
    def translate_filter(text, lang="uz", **kwargs):
        """Translate a string using the _() helper in templates.
        Usage: {{ 'hello'|t(lang) }} or {{ 'welcome'|t(lang, name=user) }}
        """
        return t(text, lang=lang, **kwargs)

    @app.context_processor
    def inject_translations():
        from flask import session, request
        lang = session.get("lang", request.cookies.get("lang", "uz"))
        if lang not in LANGUAGES:
            lang = "uz"
        dark_mode = session.get("dark_mode", request.cookies.get("dark_mode", "0") == "1")
        return {
            "_": lambda key, **kw: t(key, lang=lang, **kw),
            "lang": lang,
            "langs": LANGUAGES,
            "lang_flags": LANGUAGE_FLAGS,
            "dark_mode": dark_mode,
        }
