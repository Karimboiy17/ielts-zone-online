from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import TestAttempt
from app.extensions import mongo
from bson.objectid import ObjectId

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/")
@login_required
def profile():
    from app.cefr import score_to_cefr

    attempts = TestAttempt.get_user_attempts(current_user.id)

    # Find best CEFR level from completed tests
    best_cefr = None
    best_score = -1
    for a in attempts:
        if a.get("score") is not None and a["score"] > best_score:
            best_score = a["score"]
            if a.get("cefr_level"):
                best_cefr = {"level": a["cefr_level"], "score": a["score"]}

    # Overall CEFR from latest completed attempt
    latest_cefr = None
    completed = [a for a in attempts if a.get("score") is not None]
    if completed:
        latest = completed[0]
        if latest.get("cefr_level"):
            latest_cefr = {
                "level": latest["cefr_level"],
                "label": latest.get("cefr_label", ""),
                "score": latest["score"],
            }
        else:
            # Calculate CEFR from score if not stored
            level = score_to_cefr(latest["score"])
            latest_cefr = {
                "level": level["level"],
                "label": level["label"],
                "score": latest["score"],
            }

    # Stats by section
    reading_scores = [a["score"] for a in attempts if a.get("section") == "reading" and a.get("score") is not None]
    listening_scores = [a["score"] for a in attempts if a.get("section") == "listening" and a.get("score") is not None]
    writing_completed = [a for a in attempts if a.get("section") == "writing" and a.get("status") == "completed"]

    total_tests = len(attempts)
    completed_count = len(completed)
    best_reading = max(reading_scores) if reading_scores else None
    best_listening = max(listening_scores) if listening_scores else None

    return render_template("profile/profile.html",
                         attempts=attempts,
                         best_cefr=best_cefr,
                         latest_cefr=latest_cefr,
                         total_tests=total_tests,
                         completed=completed_count,
                         best_reading=best_reading,
                         best_listening=best_listening,
                         reading_scores=reading_scores,
                         listening_scores=listening_scores,
                         writing_completed=writing_completed)
