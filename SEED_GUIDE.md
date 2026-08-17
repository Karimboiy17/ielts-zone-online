# IELTS ZONE — Test seed moduli yozish qo'llanmasi

## ⚠️ STANDART (har bir test bunga mos bo'lishi SHART)

Yangi test kiritishdan oldin `python3.11 validate_tests.py` ishga tushiring (0 xato bo'lishi kerak).

1. **10 part**: Listening 4 (`l_p1`..`l_p4`) + Reading 5 (`r_p1`..`r_p5`) + Writing 1 (`w1`)
2. **Part raqamlari** section ichida TAKRORLANMAYDI, ketma-ket: l_p1=1..l_p4=4, r_p1=1..r_p5=5 (sub-part bo'lsa ham raqamlar davom etadi: l_p2=2, l_p2b=3)
3. **start_num** section ichida ketma-ket: har part 5 savol → 1,6,11,16,21...
4. **id konventsiyasi**: `l_p<N>`, `r_p<N>`, `w<N>` (sub-part: `l_p2b`)
5. **Har savolda javob**: multiple_group items[] da `answer` (index), matching da `answer` (list), writing gap da `gap_items`+`gap_labels`
6. **test dict**: section, title ("📗 B1 · MID" format), icon (🌱/🔰/📘/📗/📕), time_limit=55, active=True, audio_parts=[AUDIO,AUDIO,AUDIO,AUDIO]
7. **Barcha asset'lar** static/images/<section>/ va static/audio/<section>_listening_full.mp3 da bo'lishi kerak
8. **gap passage'lar** `(N) ________` formatida (template `_render_gaps` shu formatni almashtiradi)
9. **Reading Part 5** gap-MC bo'lsa: `"inline_gaps": True` (dropdown matn ichida chiqadi)
10. **Reading Part 1** notices: `"notice"` field'ga matn (rasm kesish shart emas)

Istisno: Novice testlari (novice_mid/novice_end) asl imtihon tuzilmasidan kelib chiqib boshqacha part soniga ega — validate_tests.py ularga WARN beradi (xato emas), lekin part raqamlari ketma-ket bo'lishi SHART.

## Maqsad
Bitta imtihon uchun `app/seed_<section>.py` modulini yozish, rasmlarni kesish, audioni joylashtirish.

## Ishlatiladigan python (MUHIM!)
```bash
VPY=/home/karimboy/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11
cd /home/karimboy/projects/ielts-zone-online
# pymupdf va PIL .venv da: sys.path ga qo'shish kerak
import sys; sys.path.insert(0, "/home/karimboy/projects/ielts-zone-online/.venv/lib/python3.11/site-packages")
```

## Seed modul sxemasi
```python
"""Auto-seed <SECTION> test data into MongoDB (used at app startup on Railway)."""
from datetime import datetime, timezone

AUDIO = "/static/audio/<SECTION>_listening_full.mp3"
IMG = "/static/images/<SECTION>/"

questions = [ ... ]  # 10 part: Listening 4 + Reading 5 + Writing 1

test = {
    "section": "<SECTION>",
    "title": "<TITLE>",       # masalan "📗 B1 · END"
    "icon": "📗",
    "time_limit": 55,
    "price": 0,
    "original_price": 0,
    "active": True,
    "description": "...",
    "audio_parts": [AUDIO, AUDIO, AUDIO, AUDIO],
    "created_at": datetime.now(timezone.utc),
    "questions": questions,
}

def seed_<SECTION>(db):
    """Insert or update the test document (keeps _id stable)."""
    db.tests.update_one({"section": "<SECTION>"}, {"$set": test}, upsert=True)
    return len(test["questions"])
```

## Savol formatlari (B1 MID seed'idagi kabi)

### 1. Listening Part 1 — rasmli MC (`multiple_group`)
```python
{"id": "l_p1", "type": "multiple_group", "section": "listening", "part": 1, "start_num": 1,
 "instruction": "Part 1. Questions 1-5.\n...",
 "points": 5,
 "items": [
     {"q": "1. <savol>", "option_images": [IMG + "lq1_A.png", IMG + "lq1_B.png", IMG + "lq1_C.png"],
      "options": ["A", "B", "C"], "answer": 0},
 ]}
```
- `option_images` — har bir variant uchun rasm (A/B/C), `options` = ["A","B","C"], `answer` = index (0,1,2)
- Agar savolda rasm variantlar yo'q bo'lsa (oddiy MC): faqat `q`, `options`, `answer`

### 2. Listening Part 2 — gap-fill (`writing` + gap_items)
```python
{"id": "l_p2", "type": "writing", "section": "listening", "part": 2, "start_num": 6,
 "instruction": "Part 2. Questions 6-10.\n...",
 "title": "<Matn nomi>",
 "passage": "Matn (6) ________ davom etadi (7) ________.",
 "gap_items": ["JAVOB1", "JAVOB2"], "gap_labels": ["6", "7"],
 "points": 5}
```

### 3. Listening Part 3/4 — oddiy MC yoki YES/NO (`multiple_group`)
```python
{"id": "l_p3", "type": "multiple_group", "section": "listening", "part": 3, "start_num": 11,
 "instruction": "...", "points": 5,
 "items": [{"q": "11. <savol>", "options": ["A", "B", "C"], "answer": 0}]}
```
- YES/NO uchun: `"options": ["YES", "NO"], "answer": 0/1`

### 4. Reading Part 1 — notices (`multiple_group`, notice matni qutida)
```python
{"id": "r_p1", "type": "multiple_group", "section": "reading", "part": 1, "start_num": 1,
 "instruction": "Part 1. Questions 1-5.\nLook at the text in each question. What does it say?",
 "points": 5,
 "items": [
     {"q": "1. What does it say?", "notice": "<notice matni, qatorlar \\n bilan>",
      "options": [...], "answer": idx},
 ]}
```
- Rasm kesish shart EMAS — notice matnini `notice` field'ga yozish kifoya (jadval/quti template'da chiqadi)

### 5. Reading Part 2 — matching (odamlar + 8 ta activity)
```python
{"id": "r_p2", "type": "matching", "section": "reading", "part": 2, "start_num": 6,
 "instruction": "...",
 "points": 5,
 "events": ["A Friends of Hamley Park", ...8 ta activity matni...],
 "options": ["6. <odam haqida>", "7. ...", ...],
 "items": ["A ...", "B ...", ...8 ta...],
 "answer": [4, 6, 0, 1, 2]}   # har bir odam uchun to'g'ri activity INDEXI
```
- `events` = activity'lar tavsifi (matn), `options` = odamlar tavsifi, `items` = A-H nomlari, `answer` = har bir odam uchun items indexi
- Agar odamlar rasmlari bo'lsa: `"option_images": [IMG + "p7_person6.png", ...]` qo'shish mumkin (ixtiyoriy)

### 6. Reading Part 3 — YES/NO matn ustida (`multiple_group` + passage)
```python
{"id": "r_p3", "type": "multiple_group", "section": "reading", "part": 3, "start_num": 11,
 "instruction": "...", "title": "<Matn nomi>", "passage": "<matn>", "points": 5,
 "items": [{"q": "11. <gap>", "options": ["Yes", "No"], "answer": 0}]}
```

### 7. Reading Part 4 — MC matn ustida (`multiple_group` + passage)
Xuddi Part 3, lekin options A/B/C.

### 8. Reading Part 5 — gap-fill MC, matn ichida DROPDOWN
```python
{"id": "r_p5", "type": "multiple_group", "section": "reading", "part": 5, "start_num": 21,
 "instruction": "Part 5. Questions 21-25.\nRead the text below and choose the correct answer for each gap.",
 "inline_gaps": True,
 "passage": "<matn, (21) ________ joylari bilan>",
 "points": 5,
 "items": [
     {"q": "21. <gap'li jumla>", "options": ["A", "B", "C"], "answer": idx},
 ]}
```
- `inline_gaps: True` — dropdown matn ichida chiqadi (Black Mamba uslubi)

### 9. Writing — insho (`writing`)
```python
{"id": "w1", "type": "writing", "section": "writing", "start_num": 1,
 "question": "<topshiriq matni>", "word_limit": "100", "points": 20}
```

## Rasmlarni kesish (faqat KERAK bo'lsa)
- A2 darajalari (a2_mid, a2_end) — Listening Part 1 savollari RASMDA (B1 MID (8) kabi): PDF ichidan `page.get_images()` bilan chiqarib, har savol uchun kesish kerak
- Boshqa darajalarda odatda rasm kerak emas (matn yetarli), faqat Listening Part 1 variantlari rasm bo'lsa kesish kerak

Kesish ish oqimi:
1. `page.get_pixmap(matrix=Matrix(2,2))` bilan sahifani render qil
2. `page.search_for("<matn>")` bilan matn koordinatalarini top (yoki ko'z bilan o'lchab)
3. PIL bilan crop qil, `static/images/<SECTION>/<nom>.png` ga saqla
4. Kesilgan rasmni `vision_analyze` bilan tekshir (to'liq ko'rinyaptimi)

## Javoblar kaliti
Har bir imtihon uchun javoblar alohida beriladi (vision bilan olingan). `answer` = options ichidagi INDEX (0-dan boshlab). YES/NO uchun Yes=0, No=1.

## Tekshiruv
- Modul sintaksisi: `python3.11 -m py_compile app/seed_<section>.py`
- Savollar soni javoblar kaliti bilan mos kelishi KERAK (har bir savolga javob bor)
- Natijada: fayl yozilgan + qancha part/savol bor + rasmlar ro'yxati
