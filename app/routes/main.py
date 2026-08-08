from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from app.extensions import csrf

main_bp = Blueprint("main", __name__)


def _get_lang():
    return session.get("lang", request.cookies.get("lang", "uz"))


@main_bp.route("/lang/<code>")
def set_lang(code):
    from app.translations import LANGUAGES
    if code in LANGUAGES:
        session["lang"] = code
    referrer = request.headers.get("Referer", url_for("main.index"))
    resp = redirect(referrer)
    resp.set_cookie("lang", code, max_age=365*24*3600)
    return resp


@main_bp.route("/toggle-dark", methods=["POST"])
@csrf.exempt
def toggle_dark():
    session["dark_mode"] = not session.get("dark_mode", False)
    referrer = request.headers.get("Referer", url_for("main.index"))
    resp = redirect(referrer)
    resp.set_cookie("dark_mode", "1" if session["dark_mode"] else "0", max_age=365*24*3600)
    return resp


@main_bp.route("/")
def index():
    # App-mode: students land directly on the tests page (no marketing dashboard)
    return redirect(url_for("tests.test_list"))


@main_bp.route("/about")
def about():
    return render_template("main/about.html")


@main_bp.route("/faq")
def faq():
    return render_template("main/faq.html")


@main_bp.route("/mock-guide")
def mock_guide():
    lang = _get_lang()
    # Static mock test info for guide page
    test = {
        "title_uz": "IELTS ZONE Test",
        "title_en": "IELTS ZONE Test",
        "title_ru": "IELTS ZONE Тест",
    }
    return render_template("tests/mock-guide.html", lang=lang, test=test)


@main_bp.route("/cefr")
def cefr():
    lang = _get_lang()
    levels = [
        {"code": "NOVICE", "name_uz": "Boshlang'ich", "name_en": "Novice", "name_ru": "Новичок",
         "desc_uz": "Ingliz tilini endi boshlayapman", "desc_en": "I am just starting to learn English", "desc_ru": "Я только начинаю учить английский",
         "icon": "🌱"},
        {"code": "A1", "name_uz": "Boshlang'ich", "name_en": "Beginner", "name_ru": "Начальный",
         "desc_uz": "Tushunaman va kundalik iboralarni ishlata olaman", "desc_en": "I can understand and use everyday expressions", "desc_ru": "Я понимаю и использую повседневные выражения",
         "icon": "🔰"},
        {"code": "A2", "name_uz": "Elementar", "name_en": "Elementary", "name_ru": "Элементарный",
         "desc_uz": "Tez-tez ishlatiladigan iboralarni tushunaman", "desc_en": "I can understand frequently used expressions", "desc_ru": "Я понимаю часто используемые выражения",
         "icon": "🌿"},
        {"code": "B1", "name_uz": "O'rta", "name_en": "Intermediate", "name_ru": "Средний",
         "desc_uz": "Standart mavzularda muloqot qila olaman", "desc_en": "I can communicate on standard topics", "desc_ru": "Я могу общаться на стандартные темы",
         "icon": "🌳"},
        {"code": "B1+", "name_uz": "O'rta yuqori", "name_en": "Upper Intermediate", "name_ru": "Средне-продвинутый",
         "desc_uz": "Murakkab matnlarni tushunaman va muhokama qila olaman", "desc_en": "I can understand complex texts and discuss them", "desc_ru": "Я понимаю сложные тексты и могу их обсуждать",
         "icon": "🌲"},
    ]
    return render_template("main/cefr.html", lang=lang, levels=levels)


@main_bp.route("/cefr-level")
def cefr_level():
    lang = _get_lang()
    from flask import abort
    level_code = request.args.get("code", "NOVICE")
    levels_data = {
        "NOVICE": {"code": "NOVICE", "name_uz": "Boshlang'ich", "name_en": "Novice", "name_ru": "Новичок",
               "desc_uz": "Ingliz tilini endi boshlayapman", "desc_en": "I am just starting to learn English", "desc_ru": "Я только начинаю учить английский",
               "icon": "🌱"},
        "A1": {"code": "A1", "name_uz": "Boshlang'ich", "name_en": "Beginner", "name_ru": "Начальный",
               "desc_uz": "Tushunaman va kundalik iboralarni ishlata olaman", "desc_en": "I can understand and use everyday expressions", "desc_ru": "Я понимаю и использую повседневные выражения",
               "icon": "🔰"},
        "A2": {"code": "A2", "name_uz": "Elementar", "name_en": "Elementary", "name_ru": "Элементарный",
               "desc_uz": "Tez-tez ishlatiladigan iboralarni tushunaman", "desc_en": "I can understand frequently used expressions", "desc_ru": "Я понимаю часто используемые выражения",
               "icon": "🌿"},
        "B1": {"code": "B1", "name_uz": "O'rta", "name_en": "Intermediate", "name_ru": "Средний",
               "desc_uz": "Standart mavzularda muloqot qila olaman", "desc_en": "I can communicate on standard topics", "desc_ru": "Я могу общаться на стандартные темы",
               "icon": "🌳"},
        "B1+": {"code": "B1+", "name_uz": "O'rta yuqori", "name_en": "Upper Intermediate", "name_ru": "Средне-продвинутый",
               "desc_uz": "Murakkab matnlarni tushunaman va muhokama qila olaman", "desc_en": "I can understand complex texts and discuss them", "desc_ru": "Я понимаю сложные тексты и могу их обсуждать",
               "icon": "🌲"},
    }
    level = levels_data.get(level_code)
    if not level:
        abort(404)
    modules = [
        {"id": f"{level_code.lower()}-mod-1", "title_uz": "Kirish", "title_en": "Introduction", "title_ru": "Введение",
         "lesson_count": 5},
        {"id": f"{level_code.lower()}-mod-2", "title_uz": "Asosiy mavzular", "title_en": "Main topics", "title_ru": "Основные темы",
         "lesson_count": 8},
        {"id": f"{level_code.lower()}-mod-3", "title_uz": "Amaliyot", "title_en": "Practice", "title_ru": "Практика",
         "lesson_count": 6},
    ]
    return render_template("main/cefr-level.html", lang=lang, level=level, modules=modules)


@main_bp.route("/cefr-lesson")
def cefr_lesson():
    lang = _get_lang()
    level_d = {"code": "A1", "icon": "🌱"}
    module_d = {"id": "a1-mod-1", "title_uz": "Kirish", "title_en": "Introduction", "title_ru": "Введение"}
    lesson_d = {
        "title_uz": "Alifbo va talaffuz", "title_en": "Alphabet and Pronunciation", "title_ru": "Алфавит и произношение",
        "order_num": 0,
        "content_uz": "<p>Bu darsda siz ingliz tilidagi asosiy harflar va ularning talaffuzi bilan tanishasiz.</p><p>Ingliz alifbosi 26 harfdan iborat.</p>",
        "content_en": "<p>In this lesson, you will learn the basic letters and their pronunciation.</p><p>The English alphabet has 26 letters.</p>",
        "content_ru": "<p>На этом уроке вы познакомитесь с основными буквами и их произношением.</p><p>Английский алфавит состоит из 26 букв.</p>",
    }
    qs = [
        {"question_uz": "Ingliz alifbosida nechta harf bor?", "question_en": "How many letters are in the English alphabet?", "question_ru": "Сколько букв в английском алфавите?",
         "options_uz": '["24","26","28","30"]',
         "correct_answer": 1},
    ]
    return render_template("main/cefr-lesson.html", lang=lang, lesson=lesson_d, level=level_d, module=module_d, questions=qs)


@main_bp.route("/cefr-module")
def cefr_module():
    lang = _get_lang()
    level_d = {"code": "A1", "icon": "🌱"}
    module_d = {
        "title_uz": "Kirish", "title_en": "Introduction", "title_ru": "Введение",
        "desc_uz": "Ingliz tili bilan birinchi qadamlar", "desc_en": "First steps in English", "desc_ru": "Первые шаги в английском",
    }
    lessons_d = [
        {"id": "a1-lesson-1", "title_uz": "Alifbo va talaffuz", "title_en": "Alphabet and Pronunciation", "title_ru": "Алфавит и произношение", "order_num": 0},
        {"id": "a1-lesson-2", "title_uz": "Sonlar va ranglar", "title_en": "Numbers and Colors", "title_ru": "Цифры и цвета", "order_num": 1},
        {"id": "a1-lesson-3", "title_uz": "Oila va do'stlar", "title_en": "Family and Friends", "title_ru": "Семья и друзья", "order_num": 2},
    ]
    return render_template("main/cefr-module.html", lang=lang, module=module_d, level=level_d, lessons=lessons_d)
