#!/usr/bin/env python3
"""Find all test results on Railway MongoDB."""
import sys, os
sys.path.insert(0, "/home/karimboy/projects/ielts-zone-online")
from pymongo import MongoClient

# Railway MongoDB connection (from .env style)
uri = os.getenv("MONGO_URI") or os.getenv("MONGO_URL")
if not uri:
    # local fallback for dev
    uri = "mongodb://localhost:27017/ielts_zone"

print(f"URI: {uri[:40]}...")
client = MongoClient(uri, serverSelectionTimeoutMS=8000)
db = client.get_default_database() if uri and "mongodb.railway" in uri else client["ielts_zone"]

print(f"DB: {db.name}")

print("\n=== ATTEMPTS (completed) ===")
attempts = list(db.attempts.find({"status": "completed"}).sort("completed_at", -1))
print(f"  jami: {len(attempts)}")
for a in attempts:
    user = db.users.find_one({"_id": a.get("user_id")})
    name = (user or {}).get("name", "?")
    tg = (user or {}).get("telegram_id", "?")
    section = a.get("section", "?")
    score = a.get("score", "?")
    level = a.get("cefr_level", "?")
    print(f"  {name} (TG:{tg}) | {section} | {score}% | {level}")

print("\n=== ATTEMPTS (started) ===")
started = list(db.attempts.find({"status": "started"}).sort("started_at", -1))
print(f"  jami: {len(started)}")
for a in started:
    user = db.users.find_one({"_id": a.get("user_id")})
    name = (user or {}).get("name", "?")
    tg = (user or {}).get("telegram_id", "?")
    print(f"  {name} (TG:{tg}) | {a.get('section')}")

print("\n=== STUDENTS ===")
students = list(db.students.find())
print(f"  jami: {len(students)}")
for s in students:
    print(f"  {s.get('full_name')} (TG:{s.get('tg_id')}) | tests: {len(s.get('completed_tests', []))}")
