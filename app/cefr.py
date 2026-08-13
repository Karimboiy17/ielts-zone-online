"""
IELTS ZONE online — Level Calculator
Converts test scores to IELTS ZONE levels (NOVICE, A1, A2, PRE-INTERMEDIATE, B1, B1+)

Level alignment (percentage-based):
  NOVICE:          0-16%  — Boshlang'ich (beginner)
  A1:              17-33% — Basic (can understand simple phrases)
  A2:              34-50% — Elementary (can understand common expressions)
  PRE-INTERMEDIATE: 51-66% — Pre-intermediate (can handle routine situations)
  B1:              67-83% — Intermediate (can understand routine matters)
  B1+:             84-100% — Upper-intermediate (ready for the next stage)

For Writing (teacher-scored, out of 100):
  Same thresholds apply based on total points.
"""

LEVELS = [
    {"level": "B1+", "label": "Upper-Intermediate", "min_pct": 84, "color": "#5B21B6",
     "description": "Complex texts and confident communication"},
    {"level": "B1", "label": "Intermediate", "min_pct": 67, "color": "#6D28D9",
     "description": "Routine matters in work, school, leisure"},
    {"level": "PRE-INTERMEDIATE", "label": "Pre-Intermediate", "min_pct": 51, "color": "#7C3AED",
     "description": "Can handle routine situations"},
    {"level": "A2", "label": "Elementary", "min_pct": 34, "color": "#8B5CF6",
     "description": "Frequently used expressions"},
    {"level": "A1", "label": "Basic", "min_pct": 17, "color": "#A78BFA",
     "description": "Simple everyday phrases"},
    {"level": "NOVICE", "label": "Novice", "min_pct": 0, "color": "#C4B5FD",
     "description": "Starting to learn English"},
]

# Alias for backwards compatibility
CEFR_LEVELS = LEVELS


def score_to_cefr(percentage):
    """Convert a percentage score (0-100) to a level dict."""
    for level in LEVELS:
        if percentage >= level["min_pct"]:
            return dict(level)
    return dict(LEVELS[-1])


def overall_cefr(section_scores):
    """
    Given a dict of {section_name: percentage}, compute overall level.
    Returns the lowest level across all sections (worst-case = conservative).
    """
    if not section_scores:
        return score_to_cefr(0)

    # Find the lowest level by sorting all levels by min_pct ascending
    min_level_idx = len(LEVELS) - 1  # Most basic index (NOVICE)
    for section, pct in section_scores.items():
        for i, level in enumerate(LEVELS):
            if pct >= level["min_pct"]:
                min_level_idx = min(min_level_idx, i)
                break

    return dict(LEVELS[min_level_idx])


def get_all_levels():
    """Return all levels for display purposes."""
    return [dict(level) for level in LEVELS]


def get_level_code(level_key):
    """Map section names like 'a1_mid' to level code 'A1'."""
    for code, prefix in [("B1+", "b1plus"), ("B1", "b1"), ("PRE-INTERMEDIATE", "preintermediate"),
                         ("A2", "a2"), ("A1", "a1"), ("NOVICE", "novice")]:
        if level_key.startswith(prefix):
            return code
    return None


# Exam types per level: mid and end
EXAM_TYPES = [
    {"key": "mid", "label": "MID imtihon", "icon": "📘"},
    {"key": "end", "label": "END imtihon", "icon": "📗"},
]

LEVEL_EXAMS = []
for _level in LEVELS:
    code = _level["level"].replace("+", "plus").lower()
    for _exam in EXAM_TYPES:
        LEVEL_EXAMS.append({
            "section": f"{code}_{_exam['key']}",
            "level": _level["level"],
            "level_label": _level["label"],
            "exam": _exam["key"],
            "exam_label": _exam["label"],
            "icon": _exam["icon"],
        })
