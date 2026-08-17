#!/usr/bin/env python3
"""validate_tests.py — IELTS ZONE testlarini STANDART bo'yicha tekshiradi.

Standart (SEED_GUIDE.md ga qarang):
  - 10 part: Listening 4 (l_p1..l_p4) + Reading 5 (r_p1..r_p5) + Writing 1 (w1)
  - part raqamlari section ichida TAKRORLANMASLIGI kerak (ketma-ket)
  - start_num section ichida ketma-ket (har part 5 savol: 1,6,11,16,21...)
  - har bir savolda javob bor
  - barcha static asset'lar (rasmlar/audio) mavjud
  - time_limit, audio_parts, icon, title formatlari to'g'ri

Ishlatish:  python3.11 validate_tests.py
Ogohlantirish (WARN) = standartdan og'ish, lekin bloklamaydi (novice testlari kabi).
Xato (ERROR) = tuzatish kerak.
"""
import importlib.util
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
MODS = [
    ("novice_mid", "app/seed_novice_mid.py"),
    ("novice_end", "app/seed_novice_end.py"),
    ("a1_mid", "app/seed_a1_mid.py"),
    ("a1_end", "app/seed_a1_end.py"),
    ("a2_mid", "app/seed_a2_mid.py"),
    ("a2_end", "app/seed_a2_end.py"),
    ("b1_mid", "app/seed_b1.py"),
    ("b1_end", "app/seed_b1_end.py"),
    ("b1plus_mid", "app/seed_b1plus.py"),
    ("b1plus_end", "app/seed_b1plus_end.py"),
]
ICONS = {"novice": "🌱", "a1": "🔰", "a2": "📘", "b1": "📗", "b1plus": "📕"}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BASE, path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def questions_of(m):
    if hasattr(m, "questions"):
        return m.questions
    return (getattr(m, "LISTENING_QUESTIONS", []) + getattr(m, "READING_QUESTIONS", [])
            + getattr(m, "WRITING_QUESTIONS", []))


def main():
    total_err = total_warn = 0
    for section, path in MODS:
        errs, warns = [], []
        m = load(section, path)
        qs = questions_of(m)
        test = getattr(m, "test", None)
        if test is None:
            # b1plus_mid: test dict function ichida quriladi — audio_parts modul darajasida
            test = {"audio_parts": getattr(m, "audio_parts", [])}
            for k in ("time_limit", "icon", "title"):
                test.setdefault(k, None)

        # --- title / icon ---
        level = section.rsplit("_", 1)[0]
        exp_icon = ICONS.get(level, "?")
        if test.get("icon") != exp_icon:
            warns.append(f"icon {test.get('icon')!r} != {exp_icon!r}")
        if test.get("time_limit") not in (45, 55, 70):
            warns.append(f"time_limit={test.get('time_limit')} (odatda 55)")
        if len(test.get("audio_parts", [])) != 4:
            errs.append("audio_parts 4 ta emas")
        audio = test.get("audio_parts", [""])[0]
        if not os.path.exists(BASE + audio):
            errs.append(f"audio fayl yo'q: {audio}")

        # --- structure ---
        l_parts = [q for q in qs if q.get("section") == "listening"]
        r_parts = [q for q in qs if q.get("section") == "reading"]
        w_parts = [q for q in qs if q.get("section") == "writing"]
        if len(l_parts) != 4:
            warns.append(f"listening {len(l_parts)} part (standart 4)")
        if len(r_parts) != 5:
            warns.append(f"reading {len(r_parts)} part (standart 5)")
        if len(w_parts) != 1:
            warns.append(f"writing {len(w_parts)} part (standart 1)")

        # part numbers unique per section
        for sec, parts in (("listening", l_parts), ("reading", r_parts)):
            seen = {}
            for q in parts:
                p = q.get("part")
                if p in seen:
                    errs.append(f"{sec}: part={p} takrorlanadi ({seen[p]} va {q['id']})")
                seen[p] = q["id"]

        # start_num continuity per section
        for sec, parts in (("listening", l_parts), ("reading", r_parts)):
            ordered = sorted(parts, key=lambda q: q.get("start_num", 0))
            expected = ordered[0].get("start_num", 1) if ordered else None
            for q in ordered:
                if q.get("start_num") != expected:
                    errs.append(f"{q['id']}: start_num={q.get('start_num')} (kutilgan {expected})")
                    break
                nq = (len(q.get("items") or q.get("gap_items") or [])
                      if q.get("type") != "matching" else len(q.get("options", [])))
                expected += nq

        # answers presence + assets
        refs = []
        for q in qs:
            if q.get("type") == "matching":
                nq = len(q.get("options", []))
                ans = q.get("answer")
                if not (isinstance(ans, list) and len(ans) == nq):
                    errs.append(f"{q['id']}: matching javoblar {len(ans) if ans else 0}/{nq}")
                for x in q.get("option_images", []) or []:
                    refs.append(x)
            elif q.get("type") == "writing" and q.get("gap_items"):
                if len(q.get("gap_items")) != len(q.get("gap_labels", [])):
                    errs.append(f"{q['id']}: gap_items/labels soni mos emas")
            elif q.get("type") == "writing":
                pass
            else:
                for it in q.get("items", []):
                    if not isinstance(it, dict) or "answer" not in it:
                        errs.append(f"{q['id']}: javobsiz savol")
                    for k in ("option_images", "image"):
                        v = it.get(k)
                        if isinstance(v, str):
                            refs.append(v)
                        elif isinstance(v, list):
                            refs.extend(v)
        for r in refs:
            if r.startswith("/static/") and not os.path.exists(BASE + r):
                errs.append(f"asset yo'q: {r}")

        status = "OK" if not errs else "XATO"
        print(f"{section:<14} {status}")
        for e in errs:
            print(f"    ERROR: {e}")
            total_err += 1
        for w in warns:
            print(f"    warn : {w}")
            total_warn += 1

    print("-" * 60)
    print(f"JAMI: {total_err} xato, {total_warn} ogohlantirish")
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()
