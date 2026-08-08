from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_required, current_user
from app.models import TestModel, TestAttempt
from app.extensions import mongo
from bson.objectid import ObjectId
from datetime import datetime, timezone
import json

tests_bp = Blueprint("tests", __name__)


@tests_bp.route("/")
def test_list():
    tests = TestModel.get_all()
    return render_template("tests/list.html", tests=tests)


@tests_bp.route("/<section>/")
@login_required
def test_detail(section):
    test = TestModel.get_by_section(section)
    if not test:
        flash("Test topilmadi", "error")
        return redirect(url_for("tests.test_list"))
    return render_template("tests/detail.html", test=test, section=section)


@tests_bp.route("/<section>/start", methods=["POST"])
@login_required
def start_test(section):
    test = TestModel.get_by_section(section)
    if not test:
        flash("Test topilmadi", "error")
        return redirect(url_for("tests.test_list"))

    # Create attempt — to'lov vaqtincha bekor
    attempt = TestAttempt.create(current_user.id, test["_id"], section)
    
    # If mock, redirect to mock test page
    if section == "mock":
        session["current_attempt"] = str(attempt["_id"])
        return redirect(url_for("tests.take_test", attempt_id=attempt["_id"]))

    # If writing, use per-question view
    if section == "writing":
        return redirect(url_for("tests.take_test", attempt_id=attempt["_id"]))

    # For reading/listening, store in session and redirect
    session["current_attempt"] = str(attempt["_id"])
    return redirect(url_for("tests.take_test", attempt_id=attempt["_id"]))


@tests_bp.route("/take/<attempt_id>")
@login_required
def take_test(attempt_id):
    attempt = TestAttempt.get_by_id(attempt_id)
    if not attempt or str(attempt["user_id"]) != current_user.id:
        flash("Test topilmadi", "error")
        return redirect(url_for("tests.test_list"))

    # NEW: Engnovate-style single page for level-based exams
    if attempt["section"] in ("a1_mid", "a1_end", "a2_mid", "a2_end", "b1_mid", "b1_end",
                              "b1plus_mid", "b1plus_end", "novice_mid", "novice_end"):
        return redirect(url_for("tests.take_test_all", attempt_id=attempt_id))

    test = TestModel.get_by_id(attempt["test_id"])
    
    # All objective sections use per-question view (like real exam)
    # Level-based sections (a1_mid, a1_end, ...) also use per-question view
    level_sections = ("a1_mid", "a1_end", "a2_mid", "a2_end", "b1_mid", "b1_end",
                      "b1plus_mid", "b1plus_end", "novice_mid", "novice_end")
    if attempt["section"] in ("mock", "reading", "listening", "grammar", "writing") or attempt["section"] in level_sections:
        questions = test.get("questions", [])
        if not questions:
            flash("Testda savollar yo'q", "error")
            return redirect(url_for("tests.test_list"))
        return redirect(url_for("tests.take_question", attempt_id=attempt_id, q_index=0))

    return render_template("tests/take.html", attempt=attempt, test=test)


@tests_bp.route("/take/<attempt_id>/question/<int:q_index>", methods=["GET", "POST"])
@login_required
def take_question(attempt_id, q_index):
    attempt = TestAttempt.get_by_id(attempt_id)
    if not attempt or str(attempt["user_id"]) != current_user.id:
        flash("Test topilmadi", "error")
        return redirect(url_for("tests.test_list"))

    test = TestModel.get_by_id(attempt["test_id"])
    questions = test.get("questions", [])
    total = len(questions)

    if q_index < 0 or q_index >= total:
        return redirect(url_for("tests.submit_test", attempt_id=attempt_id))

    question = questions[q_index]
    existing_answers = attempt.get("answers", [])
    prev_answer = None
    for a in existing_answers:
        if a["question_id"] == question["id"]:
            prev_answer = a
            break

    # Timer calcs — handle naive/aware datetime mismatch
    now = datetime.now(timezone.utc)
    started_at = attempt.get("started_at", now)
    if started_at.tzinfo is None:
        elapsed = (now.replace(tzinfo=None) - started_at).total_seconds()
    else:
        elapsed = (now - started_at).total_seconds()
    time_limit = test.get("time_limit", 120) * 60
    time_left = max(0, int(time_limit - elapsed))

    if request.method == "POST":
        if time_left <= 0:
            flash("⏰ Vaqt tugadi!", "warning")
            return redirect(url_for("tests.submit_test", attempt_id=attempt_id))

        # Save answer
        user_answer = None
        if question.get("type") == "writing" and question.get("writing_parts"):
            # Multiple writing parts: collect answer_0, answer_1, etc.
            part_answers = []
            for i in range(len(question.get("writing_parts", []))):
                val = request.form.get(f"answer_{i}", "").strip()
                part_answers.append(val)
            user_answer = ",".join(part_answers) if any(part_answers) else None
        elif question.get("type") == "writing" and question.get("gap_items"):
            # Gap-fill: collect answer_0, answer_1, etc.
            gap_answers = []
            for i in range(len(question.get("gap_items", []))):
                val = request.form.get(f"answer_{i}", "").strip()
                gap_answers.append(val)
            user_answer = ",".join(gap_answers) if any(gap_answers) else None
        elif question.get("type") == "writing":
            user_answer = request.form.get("answer", "").strip()
        elif question.get("type") == "multiple_group":
            # Collect answers from q0, q1, q2, etc.
            group_answers = {}
            for key, val in request.form.items():
                if key.startswith("q") and key[1:].isdigit():
                    try:
                        group_answers[key[1:]] = int(val) if val else None
                    except (ValueError, TypeError):
                        group_answers[key[1:]] = None
            user_answer = group_answers if group_answers else None
        elif question.get("type") == "matching":
            matching_answers = {}
            for key, val in request.form.items():
                if key.startswith("answer_"):
                    try:
                        idx = int(key.split("_", 1)[1])
                        matching_answers[str(idx)] = int(val) if val else None
                    except (ValueError, TypeError):
                        matching_answers[str(idx)] = None
            user_answer = matching_answers if matching_answers else None
        else:
            val = request.form.get("answer")
            if val is not None:
                try:
                    user_answer = int(val)
                except (ValueError, TypeError):
                    user_answer = None

        # Update or insert answer in attempt.answers
        updated = False
        for a in existing_answers:
            if a["question_id"] == question["id"]:
                a["user_answer"] = user_answer
                a["answered"] = True
                a["reviewed"] = request.form.get("reviewed") == "1"
                updated = True
                break
        if not updated:
            existing_answers.append({
                "question_id": question["id"],
                "section": question.get("section", "mock"),
                "user_answer": user_answer,
                "answered": True,
                "reviewed": request.form.get("reviewed") == "1",
            })

        TestAttempt.update(attempt_id, {"answers": existing_answers})

        # Next, previous or submit
        go_prev = request.form.get("go_prev")
        go_target = request.form.get("go_target")
        if go_target is not None:
            try:
                target = int(go_target)
                if target < 0: target = 0
                if target >= total: target = total - 1
                return redirect(url_for("tests.take_question", attempt_id=attempt_id, q_index=target))
            except (ValueError, TypeError):
                pass
        if q_index + 1 >= total:
            return redirect(url_for("tests.submit_test", attempt_id=attempt_id))
        return redirect(url_for("tests.take_question", attempt_id=attempt_id, q_index=q_index + 1))

    return render_template("tests/mock-question.html",
                         attempt=attempt,
                         test=test,
                         question=question,
                         q_index=q_index,
                         total=total,
                         prev_answer=prev_answer,
                         time_left=time_left,
                         audio_parts=test.get("audio_parts", []))


@tests_bp.route("/take/<attempt_id>/writing")
@login_required
def take_writing(attempt_id):
    attempt = TestAttempt.get_by_id(attempt_id)
    if not attempt or str(attempt["user_id"]) != current_user.id:
        flash("Test topilmadi", "error")
        return redirect(url_for("tests.test_list"))

    test = TestModel.get_by_id(attempt["test_id"])
    return render_template("tests/writing.html", attempt=attempt, test=test)


@tests_bp.route("/submit/<attempt_id>", methods=["GET", "POST"])
@login_required
def submit_test(attempt_id):
    attempt = TestAttempt.get_by_id(attempt_id)
    if not attempt or str(attempt["user_id"]) != current_user.id:
        return {"error": "Not found"}, 404

    test = TestModel.get_by_id(attempt["test_id"])
    section = attempt["section"]

    if section == "mock":
        # Per-section scoring for mock test — read from pre-stored answers
        sections = {"reading": {"answers": [], "earned": 0, "total": 0},
                     "listening": {"answers": [], "earned": 0, "total": 0},
                     "grammar": {"answers": [], "earned": 0, "total": 0}}
        writing_answers = []
        stored_answers = attempt.get("answers", [])
        answers_map = {a["question_id"]: a for a in stored_answers}

        for q in test["questions"]:
            qid = q["id"]
            qsection = q.get("section", section)
            stored = answers_map.get(qid)

            if q.get("type") == "writing":
                answer_text = ""
                if stored and stored.get("answered"):
                    answer_text = stored.get("user_answer", "")
                writing_answers.append({
                    "question_id": qid, "answer": answer_text,
                    "user_answer": None, "correct": None,
                    "points_possible": q["points"], "section": "writing"
                })
            else:
                correct = False
                if stored and stored.get("answered") and stored.get("user_answer") is not None:
                    try:
                        if q.get("type") == "matching":
                            # user_answer is a dict like {"0": "7", "1": "10"} where key=option_idx, value=item_number
                            user_ans = stored["user_answer"]
                            if isinstance(user_ans, dict):
                                correct_ans = q["answer"]
                                match_count = 0
                                for opt_idx, expected_item in enumerate(correct_ans):
                                    key = str(opt_idx)
                                    if key in user_ans and user_ans[key] is not None:
                                        try:
                                            if int(user_ans[key]) == int(expected_item):
                                                match_count += 1
                                        except (ValueError, TypeError):
                                            pass
                                correct = match_count == len(correct_ans) if correct_ans else False
                            elif isinstance(user_ans, list):
                                correct_ans = q["answer"]
                                if isinstance(correct_ans, list):
                                    match_count = sum(1 for i, a in enumerate(user_ans) if i < len(correct_ans) and str(a).strip() == str(correct_ans[i]).strip())
                                    correct = match_count == len(correct_ans)
                                else:
                                    correct = False
                            else:
                                correct = False
                        else:
                            # multiple, true_false, true_false_not_given
                            correct = (int(stored["user_answer"]) == int(q["answer"]))
                    except (ValueError, TypeError, json.JSONDecodeError):
                        pass
                ans = {
                    "question_id": qid, "section": qsection,
                    "user_answer": stored.get("user_answer") if stored else None,
                    "correct": correct,
                    "correct_answer": q.get("answer"),
                    "points_earned": q["points"] if correct else 0,
                    "points_possible": q["points"],
                }
                sections[qsection]["answers"].append(ans)
                sections[qsection]["total"] += q["points"]
                if correct:
                    sections[qsection]["earned"] += q["points"]

        reading_pct = round((sections["reading"]["earned"] / sections["reading"]["total"]) * 100) if sections["reading"]["total"] > 0 else 0
        listening_pct = round((sections["listening"]["earned"] / sections["listening"]["total"]) * 100) if sections["listening"]["total"] > 0 else 0
        grammar_pct = round((sections["grammar"]["earned"] / sections["grammar"]["total"]) * 100) if sections["grammar"]["total"] > 0 else 0
        all_earned = sections["reading"]["earned"] + sections["listening"]["earned"] + sections["grammar"]["earned"]
        all_total = sections["reading"]["total"] + sections["listening"]["total"] + sections["grammar"]["total"]
        overall_pct = round((all_earned / all_total) * 100) if all_total > 0 else 0

        from app.cefr import score_to_cefr
        reading_cefr = score_to_cefr(reading_pct)
        listening_cefr = score_to_cefr(listening_pct)
        grammar_cefr = score_to_cefr(grammar_pct)
        overall_cefr = score_to_cefr(overall_pct)

        all_answers = sections["reading"]["answers"] + sections["listening"]["answers"] + sections["grammar"]["answers"] + writing_answers

        TestAttempt.update(attempt_id, {
            "answers": all_answers,
            "score": overall_pct,
            "earned_points": all_earned,
            "total_points": all_total,
            "reading_score": reading_pct,
            "listening_score": listening_pct,
            "grammar_score": grammar_pct,
            "reading_cefr": reading_cefr["level"],
            "listening_cefr": listening_cefr["level"],
            "grammar_cefr": grammar_cefr["level"],
            "cefr_level": overall_cefr["level"],
            "cefr_label": overall_cefr["label"],
            "status": "completed",
            "completed_at": datetime.now(timezone.utc),
        })

        mongo.db.users.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$inc": {"test_count": 1}}
        )
        return redirect(url_for("tests.result", attempt_id=attempt_id))

    if section == "writing":
        # Save writing answers for manual review (from pre-stored answers)
        answers = []
        stored_answers = attempt.get("answers", [])
        answers_map = {a["question_id"]: a for a in stored_answers}
        for q in test["questions"]:
            qid = q["id"]
            stored = answers_map.get(qid)
            answer_text = ""
            if stored and stored.get("answered"):
                ua = stored.get("user_answer", "")
                answer_text = ua if isinstance(ua, str) else str(ua)
            answers.append({
                "question_id": qid,
                "answer": answer_text,
                "points_possible": q["points"],
            })

        TestAttempt.update(attempt_id, {
            "answers": answers,
            "status": "writing_review",
            "completed_at": datetime.now(timezone.utc),
        })
        flash("✅ Writing javoblaringiz qabul qilindi. Natija 2 kun ichida tekshiriladi.", "success")
        return redirect(url_for("tests.result", attempt_id=attempt_id))

    else:
        # Auto-grade from pre-stored answers (per-question view saves on each 'Next')
        answers = []
        total = 0
        earned = 0
        stored_answers = attempt.get("answers", [])
        answers_map = {a["question_id"]: a for a in stored_answers}

        for q in test["questions"]:
            qid = q["id"]
            stored = answers_map.get(qid)
            correct = False
            if stored and stored.get("answered") and stored.get("user_answer") is not None:
                try:
                    if q.get("type") == "matching":
                        # user_answer is a dict like {"0": "3", "1": "4"} where key=option_idx, value=item_idx
                        user_ans = stored["user_answer"]
                        if isinstance(user_ans, dict):
                            correct_ans = q["answer"]
                            match_count = 0
                            for opt_idx, expected_item in enumerate(correct_ans):
                                key = str(opt_idx)
                                if key in user_ans and user_ans[key] is not None:
                                    try:
                                        if int(user_ans[key]) == int(expected_item):
                                            match_count += 1
                                    except (ValueError, TypeError):
                                        pass
                            correct = match_count == len(correct_ans) if correct_ans else False
                        elif isinstance(user_ans, list):
                            correct_ans = q["answer"]
                            if isinstance(correct_ans, list):
                                match_count = sum(1 for i, a in enumerate(user_ans) if i < len(correct_ans) and str(a).strip() == str(correct_ans[i]).strip())
                                correct = match_count == len(correct_ans)
                            else:
                                correct = False
                        else:
                            correct = False
                    elif q.get("type") == "writing" and q.get("gap_items"):
                        # Gap-fill: compare each answer case-insensitively
                        user_ans = stored["user_answer"]
                        if isinstance(user_ans, str):
                            parts = user_ans.split(",")
                            correct_items = q.get("gap_items", [])
                            match_count = 0
                            for i, correct_word in enumerate(correct_items):
                                if i < len(parts):
                                    user_word = parts[i].strip().lower()
                                    if user_word == correct_word.lower():
                                        match_count += 1
                            correct = match_count == len(correct_items) if correct_items else False
                        else:
                            correct = False
                    elif q.get("type") == "multiple_group":
                        user_ans = stored["user_answer"]
                        if isinstance(user_ans, dict):
                            items = q.get("items", [])
                            match_count = 0
                            for i, item in enumerate(items):
                                key = f"q{i}"
                                if key in user_ans and user_ans[key] is not None:
                                    try:
                                        if int(user_ans[key]) == int(item.get("answer")):
                                            match_count += 1
                                    except (ValueError, TypeError):
                                        pass
                            correct = match_count == len(items) if items else False
                        else:
                            correct = False
                    else:
                        # multiple, true_false, true_false_not_given
                        correct = (int(stored["user_answer"]) == q["answer"])
                except (ValueError, TypeError, json.JSONDecodeError):
                    pass

            answers.append({
                "question_id": qid,
                "user_answer": stored.get("user_answer") if stored else None,
                "correct": correct,
                "correct_answer": q.get("answer"),
                "points_earned": q["points"] if correct else 0,
                "points_possible": q["points"],
            })
            total += q["points"]
            if correct:
                earned += q["points"]

        percentage = round((earned / total) * 100) if total > 0 else 0
        from app.cefr import score_to_cefr
        cefr_level = score_to_cefr(percentage)

        TestAttempt.update(attempt_id, {
            "answers": answers,
            "score": percentage,
            "total_points": total,
            "earned_points": earned,
            "status": "completed",
            "cefr_level": cefr_level["level"],
            "cefr_label": cefr_level["label"],
            "completed_at": datetime.now(timezone.utc),
        })

        # Update user test count
        mongo.db.users.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$inc": {"test_count": 1}}
        )

        return redirect(url_for("tests.result", attempt_id=attempt_id))


@tests_bp.route("/result/<attempt_id>")
@login_required
def result(attempt_id):
    attempt = TestAttempt.get_by_id(attempt_id)
    if not attempt or str(attempt["user_id"]) != current_user.id:
        flash("Natija topilmadi", "error")
        return redirect(url_for("tests.test_list"))

    test = TestModel.get_by_id(attempt["test_id"])
    if not test:
        flash("Test topilmadi (o'chirilgan bo'lishi mumkin)", "error")
        return redirect(url_for("tests.test_list"))

    # Calculate stats for reading/listening/mock
    if attempt.get("section") == "mock":
        correct_count = 0
        total_questions = 0
        reading_correct = 0
        reading_total = 0
        listening_correct = 0
        listening_total = 0
        grammar_correct = 0
        grammar_total = 0
        if attempt.get("answers"):
            for a in attempt["answers"]:
                if a.get("section") == "writing":
                    continue
                total_questions += 1
                if a.get("section") == "reading":
                    reading_total += 1
                    if a.get("correct"):
                        reading_correct += 1
                        correct_count += 1
                elif a.get("section") == "listening":
                    listening_total += 1
                    if a.get("correct"):
                        listening_correct += 1
                        correct_count += 1
                elif a.get("section") == "grammar":
                    grammar_total += 1
                    if a.get("correct"):
                        grammar_correct += 1
                        correct_count += 1
                else:
                    if a.get("correct"):
                        correct_count += 1

        return render_template("tests/result.html",
                             attempt=attempt,
                             test=test,
                             correct_count=correct_count,
                             total_questions=total_questions,
                             reading_correct=reading_correct,
                             reading_total=reading_total,
                             listening_correct=listening_correct,
                             listening_total=listening_total,
                             grammar_correct=grammar_correct,
                             grammar_total=grammar_total)

    # Calculate stats for reading/listening
    correct_count = 0
    total_questions = 0
    if attempt.get("answers"):
        for a in attempt["answers"]:
            total_questions += 1
            if a.get("correct"):
                correct_count += 1

    return render_template("tests/result.html",
                         attempt=attempt,
                         test=test,
                         correct_count=correct_count,
                         total_questions=total_questions)


# ============ ENG-NOVATE STYLE: single-page all-parts test ============

def _render_gaps(q, qi):
    """Replace (N) ________ placeholders in passage with inline inputs."""
    import re
    passage = q.get("passage", "")
    gap_items = q.get("gap_items", [])
    gap_labels = q.get("gap_labels", []) or [str(i + 1) for i in range(len(gap_items))]

    def repl(m):
        label = m.group(1)
        try:
            idx = gap_labels.index(label)
        except ValueError:
            return m.group(0)
        return (f'<span class="gap-wrap"><span class="gap-num">{label}.</span>'
                f'<input type="text" name="q{qi}_g{idx}" class="gap-input" '
                f'autocomplete="off" value=""></span>')

    return re.sub(r"\((\d+)\)\s*_+", repl, passage)


def _render_paragraphs(passage):
    """Split passage into <p> paragraphs, preserving original breaks."""
    import re
    paragraphs = re.split(r"\n\s*\n", passage.strip())
    parts = []
    for p in paragraphs:
        p = p.strip()
        if p:
            # Handle single newlines inside a paragraph -> <br>
            p_html = p.replace("\n", "<br>")
            parts.append(f"<p style='margin:0 0 12px;'>{p_html}</p>")
    return "\n".join(parts)


def _render_mc_gaps(passage, items, qi):
    """Replace (N) ____ placeholders with inline <select> dropdowns from items."""
    import re
    def repl(m):
        label = m.group(1)
        # find item whose question contains this label
        for ii, item in enumerate(items):
            qtext = item.get("q", "")
            if re.search(rf"\(?\b{label}\b\)?", qtext.split(".")[0] + ".") or qtext.startswith(label + "."):
                opts = item.get("options", [])
                options_html = '<option value="">—</option>'
                for oi, opt in enumerate(opts):
                    options_html += f'<option value="{oi}">{opt}</option>'
                return (f'<select name="q{qi}_i{ii}" class="gap-select">'
                        f'{options_html}</select>')
        return m.group(0)
    return re.sub(r"\((\d+)\)\s*_+", repl, passage)


@tests_bp.route("/take/<attempt_id>/all")
@login_required
def take_test_all(attempt_id):
    """Engnovate-style single-page test: all parts on one scrollable page."""
    attempt = TestAttempt.get_by_id(attempt_id)
    if not attempt or str(attempt["user_id"]) != current_user.id:
        flash("Test topilmadi", "error")
        return redirect(url_for("tests.test_list"))

    test = TestModel.get_by_id(attempt["test_id"])
    if not test:
        flash("Test topilmadi (o'chirilgan bo'lishi mumkin)", "error")
        return redirect(url_for("tests.test_list"))

    questions = test.get("questions", [])
    audio_parts = test.get("audio_parts", [])

    # Prepare per-question rendered passage with inline gap inputs
    prepared = []
    for qi, q in enumerate(questions):
        q = dict(q)
        if q.get("type") == "writing" and q.get("gap_items"):
            q["rendered_passage"] = _render_gaps(q, qi)
        # MC gap-fill (Black Mamba style): passage with inline dropdowns
        if q.get("inline_gaps"):
            q["rendered_mc_passage"] = _render_mc_gaps(q.get("passage", ""), q.get("items", []), qi)
        # Render passage paragraphs as <p> tags (keep original paragraph breaks)
        if q.get("passage"):
            q["rendered_paragraphs"] = _render_paragraphs(q["passage"])
        prepared.append(q)

    # Timer
    now = datetime.now(timezone.utc)
    started_at = attempt.get("started_at", now)
    if started_at.tzinfo is None:
        elapsed = (now.replace(tzinfo=None) - started_at).total_seconds()
    else:
        elapsed = (now - started_at).total_seconds()
    time_limit = test.get("time_limit", 120) * 60
    time_left = max(0, int(time_limit - elapsed))

    return render_template("tests/engnovate-take.html",
                         attempt=attempt, test=test, questions=prepared,
                         audio_parts=audio_parts,
                         time_left=time_left)


@tests_bp.route("/take/<attempt_id>/all/submit", methods=["POST"])
@login_required
def submit_test_all(attempt_id):
    """Collect all answers from the single-page form, grade, save."""
    attempt = TestAttempt.get_by_id(attempt_id)
    if not attempt or str(attempt["user_id"]) != current_user.id:
        flash("Test topilmadi", "error")
        return redirect(url_for("tests.test_list"))

    test = TestModel.get_by_id(attempt["test_id"])
    if not test:
        flash("Test topilmadi", "error")
        return redirect(url_for("tests.test_list"))

    questions = test.get("questions", [])
    answers = []
    total = 0
    earned = 0

    for qi, q in enumerate(questions):
        qid = q["id"]
        qtype = q.get("type")
        user_answer = None
        correct = False

        if qtype == "writing" and q.get("gap_items"):
            parts = []
            for gi in range(len(q.get("gap_items", []))):
                val = request.form.get(f"q{qi}_g{gi}", "").strip()
                parts.append(val)
            user_answer = ",".join(parts) if any(parts) else None
            if user_answer:
                correct_items = q.get("gap_items", [])
                match = sum(1 for i, w in enumerate(correct_items)
                            if i < len(parts) and parts[i].strip().lower() == w.lower())
                correct = match == len(correct_items) if correct_items else False

        elif qtype == "writing":
            user_answer = request.form.get(f"q{qi}_answer", "").strip() or None
            correct = False  # teacher review

        elif qtype == "multiple_group":
            group = {}
            for ii in range(len(q.get("items", []))):
                val = request.form.get(f"q{qi}_i{ii}")
                if val is not None:
                    try:
                        group[str(ii)] = int(val)
                    except (ValueError, TypeError):
                        group[str(ii)] = None
            user_answer = group if group else None
            if user_answer:
                items = q.get("items", [])
                match = sum(1 for i, item in enumerate(items)
                            if str(i) in user_answer and user_answer[str(i)] is not None
                            and int(user_answer[str(i)]) == int(item.get("answer")))
                correct = match == len(items) if items else False

        elif qtype == "matching":
            match_map = {}
            for oi in range(len(q.get("options", []))):
                val = request.form.get(f"q{qi}_o{oi}")
                if val not in (None, ""):
                    try:
                        match_map[str(oi)] = int(val)
                    except (ValueError, TypeError):
                        match_map[str(oi)] = None
            user_answer = match_map if match_map else None
            if user_answer:
                correct_ans = q.get("answer", [])
                match = sum(1 for oi, expected in enumerate(correct_ans)
                            if str(oi) in user_answer and user_answer[str(oi)] is not None
                            and int(user_answer[str(oi)]) == int(expected))
                correct = match == len(correct_ans) if correct_ans else False

        elif qtype in ("multiple", "true_false", "true_false_not_given"):
            val = request.form.get(f"q{qi}_answer")
            if val not in (None, ""):
                try:
                    user_answer = int(val)
                except (ValueError, TypeError):
                    user_answer = None
                correct = user_answer == q.get("answer")

        qpoints = q.get("points", 1)
        total += qpoints
        if correct:
            earned += qpoints
        answers.append({
            "question_id": qid,
            "user_answer": user_answer,
            "correct": correct,
            "correct_answer": q.get("answer"),
            "points_earned": qpoints if correct else 0,
            "points_possible": qpoints,
            "answered": user_answer is not None,
        })

    percentage = round((earned / total) * 100) if total > 0 else 0
    from app.cefr import score_to_cefr
    level = score_to_cefr(percentage)

    TestAttempt.update(attempt_id, {
        "answers": answers,
        "score": percentage,
        "total_points": total,
        "earned_points": earned,
        "status": "completed",
        "cefr_level": level["level"],
        "cefr_label": level["label"],
        "completed_at": datetime.now(timezone.utc),
    })
    mongo.db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$inc": {"test_count": 1}}
    )
    return redirect(url_for("tests.result", attempt_id=attempt_id))
