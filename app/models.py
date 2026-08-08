from app.extensions import mongo, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime, timezone


class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data

    @property
    def id(self):
        return str(self.user_data["_id"])

    @property
    def username(self):
        return self.user_data.get("username", "")

    @property
    def name(self):
        return self.user_data.get("name", self.user_data.get("username", ""))

    @property
    def email(self):
        return self.user_data.get("email", "")

    @property
    def telegram(self):
        return self.user_data.get("telegram", "")

    @property
    def telegram_id(self):
        return self.user_data.get("telegram_id")

    @property
    def phone(self):
        return self.user_data.get("phone", "")

    @property
    def is_admin(self):
        return self.user_data.get("role") == "admin"

    @property
    def created_at(self):
        return self.user_data.get("created_at")

    @staticmethod
    def get_by_id(user_id):
        data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User(data) if data else None

    @staticmethod
    def get_by_email(email):
        data = mongo.db.users.find_one({"email": email.lower().strip()})
        return User(data) if data else None

    @staticmethod
    def get_by_username(username):
        data = mongo.db.users.find_one({"username": username.strip()})
        return User(data) if data else None

    @staticmethod
    def get_by_telegram_id(tg_id):
        data = mongo.db.users.find_one({"telegram_id": str(tg_id)})
        return User(data) if data else None

    @staticmethod
    def create(name, email, password, telegram="", username=""):
        if not username:
            username = email.split("@")[0]
        user = {
            "name": name.strip(),
            "username": username.strip(),
            "email": email.lower().strip(),
            "password": generate_password_hash(password),
            "telegram": telegram.strip(),
            "role": "user",
            "created_at": datetime.now(timezone.utc),
            "test_count": 0,
        }
        result = mongo.db.users.insert_one(user)
        user["_id"] = result.inserted_id
        try:
            from app.data_manager import log_user_to_sheet
            log_user_to_sheet(name, email, telegram or "")
        except Exception:
            pass
        return User(user)

    def check_password(self, password):
        return check_password_hash(self.user_data["password"], password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "telegram": self.telegram,
            "role": self.user_data.get("role", "user"),
            "test_count": self.user_data.get("test_count", 0),
            "created_at": self.created_at,
        }


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


# ===== TEST Models =====

DEFAULT_TESTS = {
    "reading": {
        "title": "Reading",
        "icon": "📖",
        "time_limit": 60,
        "price": 0,
        "original_price": 25000,
        "questions": [
            {
                "id": "r1",
                "type": "multiple",
                "question": "What is the main purpose of the text?",
                "passage": "Climate change is one of the most pressing issues of our time. Scientists around the world agree that human activities, particularly the burning of fossil fuels, are causing global temperatures to rise. This has led to melting ice caps, rising sea levels, and more frequent extreme weather events. Governments worldwide are now working to reduce carbon emissions and transition to renewable energy sources.",
                "options": [
                    "A) To discuss the beauty of nature",
                    "B) To explain climate change and its effects",
                    "C) To promote fossil fuels",
                    "D) To describe weather patterns"
                ],
                "answer": 1,
                "points": 1
            },
            {
                "id": "r2",
                "type": "multiple",
                "question": "According to the text, what is causing global temperatures to rise?",
                "passage": "",
                "options": [
                    "A) Natural weather cycles",
                    "B) Human activities like burning fossil fuels",
                    "C) Volcanic eruptions",
                    "D) Ocean currents"
                ],
                "answer": 1,
                "points": 1
            },
            {
                "id": "r3",
                "type": "multiple",
                "question": "What are governments doing to address the problem?",
                "passage": "",
                "options": [
                    "A) Ignoring the issue",
                    "B) Increasing fossil fuel production",
                    "C) Reducing carbon emissions and using renewable energy",
                    "D) Building more factories"
                ],
                "answer": 2,
                "points": 1
            },
            {
                "id": "r4",
                "type": "multiple",
                "question": "The word 'transition' in the text most closely means:",
                "passage": "",
                "options": [
                    "A) Stop",
                    "B) Change or shift",
                    "C) Destroy",
                    "D) Maintain"
                ],
                "answer": 1,
                "points": 1
            },
            {
                "id": "r5",
                "type": "multiple",
                "question": "Which of the following is NOT mentioned as an effect of climate change?",
                "passage": "",
                "options": [
                    "A) Melting ice caps",
                    "B) Rising sea levels",
                    "C) Increased biodiversity",
                    "D) Extreme weather events"
                ],
                "answer": 2,
                "points": 1
            }
        ]
    },
    "listening": {
        "title": "Listening",
        "icon": "🎧",
        "time_limit": 40,
        "price": 0,
        "original_price": 25000,
        "questions": [
            {
                "id": "l1",
                "type": "multiple",
                "question": "What is the speaker's main topic?",
                "passage": "Listen to the following lecture about artificial intelligence. (In a real test, audio would play here. For now, read the transcript.) Artificial intelligence has transformed many industries. From healthcare to transportation, AI systems are helping humans make better decisions. However, there are concerns about job displacement and privacy.",
                "options": [
                    "A) History of computers",
                    "B) Impact of artificial intelligence",
                    "C) How to program",
                    "D) Internet security"
                ],
                "answer": 1,
                "points": 1
            },
            {
                "id": "l2",
                "type": "multiple",
                "question": "Which industries are mentioned as being transformed by AI?",
                "passage": "",
                "options": [
                    "A) Agriculture and mining",
                    "B) Healthcare and transportation",
                    "C) Fashion and entertainment",
                    "D) Education and sports"
                ],
                "answer": 1,
                "points": 1
            },
            {
                "id": "l3",
                "type": "multiple",
                "question": "What concerns about AI does the speaker mention?",
                "passage": "",
                "options": [
                    "A) Cost and speed",
                    "B) Job displacement and privacy",
                    "C) Language barriers",
                    "D) Energy consumption"
                ],
                "answer": 1,
                "points": 1
            },
            {
                "id": "l4",
                "type": "multiple",
                "question": "The speaker's attitude towards AI can be described as:",
                "passage": "",
                "options": [
                    "A) Completely negative",
                    "B) Balanced — acknowledging benefits and concerns",
                    "C) Enthusiastic without reservations",
                    "D) Indifferent"
                ],
                "answer": 1,
                "points": 1
            },
            {
                "id": "l5",
                "type": "multiple",
                "question": "What does the speaker say AI helps humans do?",
                "passage": "",
                "options": [
                    "A) Work faster",
                    "B) Make better decisions",
                    "C) Save money",
                    "D) Learn languages"
                ],
                "answer": 1,
                "points": 1
            }
        ]
    },
    "grammar": {
        "title": "Grammar",
        "icon": "📐",
        "time_limit": 30,
        "price": 0,
        "original_price": 25000,
        "questions": [
            {
                "id": "g1",
                "type": "multiple",
                "question": "Choose the correct option to complete the sentence: She ___ to school every day.",
                "passage": "",
                "options": ["A) go", "B) goes", "C) going", "D) gone"],
                "answer": 1,
                "points": 1
            },
            {
                "id": "g2",
                "type": "multiple",
                "question": "Find the error in the sentence: 'He don't like coffee.'",
                "passage": "",
                "options": ["A) He", "B) don't", "C) like", "D) No error"],
                "answer": 1,
                "points": 1
            },
            {
                "id": "g3",
                "type": "multiple",
                "question": "Choose the correct word: The ___ of the research were published last week.",
                "passage": "",
                "options": ["A) find", "B) found", "C) findings", "D) founder"],
                "answer": 2,
                "points": 1
            }
        ]
    },
    "writing": {
        "title": "Writing",
        "icon": "✍️",
        "time_limit": 60,
        "price": 0,
        "original_price": 25000,
        "questions": [
            {
                "id": "w1",
                "type": "writing",
                "question": "Task 1: Write an email to your manager requesting time off for a personal matter. Include: reason for leave, dates, and how you will handle your responsibilities before leaving.",
                "word_limit": "150-200",
                "points": 10
            },
            {
                "id": "w2",
                "type": "writing",
                "question": "Task 2: Some people believe that social media has a negative impact on society. Others think it brings people together. Discuss both views and give your opinion.",
                "word_limit": "200-300",
                "points": 15
            }
        ]
    },
    "mock": {
        "title": "IELTS ZONE Test",
        "icon": "🎯",
        "time_limit": 120,
        "price": 60000,
        "original_price": 100000,
        "description": "To'liq IELTS imtihoni: Reading + Listening + Writing + Speaking",
        "questions": [
            {"id": "r1", "type": "multiple", "section": "reading", "question": "What is the main purpose...", "passage": "Climate change is one of the most pressing issues...", "options": ["A) To discuss nature", "B) To explain climate change", "C) To promote fossil fuels", "D) To describe weather"], "answer": 1, "points": 1},
            {"id": "r2", "type": "multiple", "section": "reading", "question": "What is causing global temperatures to rise?", "passage": "", "options": ["A) Natural cycles", "B) Human activities", "C) Volcanoes", "D) Ocean currents"], "answer": 1, "points": 1},
            {"id": "r3", "type": "multiple", "section": "reading", "question": "What are governments doing?", "passage": "", "options": ["A) Ignoring", "B) Increasing fossil fuels", "C) Reducing emissions, using renewables", "D) Building factories"], "answer": 2, "points": 1},
            {"id": "r4", "type": "multiple", "section": "reading", "question": "'Transition' most closely means:", "passage": "", "options": ["A) Stop", "B) Change or shift", "C) Destroy", "D) Maintain"], "answer": 1, "points": 1},
            {"id": "r5", "type": "multiple", "section": "reading", "question": "Which is NOT an effect of climate change?", "passage": "", "options": ["A) Melting ice caps", "B) Rising sea levels", "C) Better crop yields", "D) Extreme weather"], "answer": 2, "points": 1},
            {"id": "l1", "type": "multiple", "section": "listening", "question": "What is the speaker's main topic?", "passage": "Artificial intelligence has transformed many industries.", "options": ["A) History of computers", "B) Impact of AI", "C) How to program", "D) Internet security"], "answer": 1, "points": 1},
            {"id": "l2", "type": "multiple", "section": "listening", "question": "Which industries are transformed by AI?", "passage": "", "options": ["A) Agriculture", "B) Healthcare & transportation", "C) Fashion", "D) Education"], "answer": 1, "points": 1},
            {"id": "l3", "type": "multiple", "section": "listening", "question": "What concerns about AI are mentioned?", "passage": "", "options": ["A) Cost and speed", "B) Job displacement and privacy", "C) Language barriers", "D) Energy"], "answer": 1, "points": 1},
            {"id": "l4", "type": "multiple", "section": "listening", "question": "Speaker's attitude towards AI?", "passage": "", "options": ["A) Negative", "B) Balanced", "C) Enthusiastic only", "D) Indifferent"], "answer": 1, "points": 1},
            {"id": "l5", "type": "multiple", "section": "listening", "question": "What does AI help humans do?", "passage": "", "options": ["A) Work faster", "B) Make better decisions", "C) Save money", "D) Learn languages"], "answer": 1, "points": 1},
            {"id": "g1", "type": "multiple", "section": "grammar", "question": "She ___ to school every day.", "passage": "", "options": ["A) go", "B) goes", "C) going", "D) gone"], "answer": 1, "points": 1},
            {"id": "g2", "type": "multiple", "section": "grammar", "question": "Find the error: 'He don't like coffee.'", "passage": "", "options": ["A) He", "B) don't", "C) like", "D) No error"], "answer": 1, "points": 1},
            {"id": "g3", "type": "multiple", "section": "grammar", "question": "The ___ of the research were published.", "passage": "", "options": ["A) find", "B) found", "C) findings", "D) founder"], "answer": 2, "points": 1},
            {"id": "w1", "type": "writing", "section": "writing", "question": "Task 1: Write an email to your manager requesting time off.", "word_limit": "150-200", "points": 10},
            {"id": "w2", "type": "writing", "section": "writing", "question": "Task 2: Social media — negative impact or brings people together? Discuss both views.", "word_limit": "200-300", "points": 15}
        ]
    }
}


class TestModel:
    @staticmethod
    def get_all():
        """Return all available test types. No side effects."""
        return list(mongo.db.tests.find({}))

    @staticmethod
    def get_by_section(section):
        return mongo.db.tests.find_one({"section": section, "active": True})

    @staticmethod
    def get_by_id(test_id):
        return mongo.db.tests.find_one({"_id": ObjectId(test_id)})

class TestAttempt:
    @staticmethod
    def create(user_id, test_id, section):
        # Generate unique 6-digit payment code
        import random
        while True:
            code = str(random.randint(100000, 999999))
            if not mongo.db.attempts.find_one({"payment_code": code}):
                break
        attempt = {
            "user_id": ObjectId(user_id),
            "test_id": ObjectId(test_id) if not isinstance(test_id, ObjectId) else test_id,
            "section": section,
            "status": "started",  # started, paid, completed, writing_review
            "answers": [],
            "score": None,
            "total_points": 0,
            "earned_points": 0,
            "payment_status": "unpaid",  # unpaid, checking, paid
            "payment_code": code,
            "payment_receipt": "",
            "receipt_file_id": None,
            "tg_chat_id": None,
            "started_at": datetime.now(timezone.utc),
            "completed_at": None,
            "paid_at": None,
        }
        result = mongo.db.attempts.insert_one(attempt)
        attempt["_id"] = result.inserted_id
        return attempt

    @staticmethod
    def get_by_id(attempt_id):
        return mongo.db.attempts.find_one({"_id": ObjectId(attempt_id)})

    @staticmethod
    def get_user_attempts(user_id, limit=20):
        return list(mongo.db.attempts.find(
            {"user_id": ObjectId(user_id)}
        ).sort("started_at", -1).limit(limit))

    @staticmethod
    def update(attempt_id, data):
        return mongo.db.attempts.update_one(
            {"_id": ObjectId(attempt_id)},
            {"$set": data}
        )


class WritingSubmission:
    @staticmethod
    def get_pending():
        return list(mongo.db.attempts.find({
            "section": "writing",
            "status": "writing_review",
            "payment_status": "paid"
        }).sort("completed_at", 1))

    @staticmethod
    def get_all_checked():
        return list(mongo.db.attempts.find({
            "section": "writing",
            "status": "completed"
        }).sort("completed_at", -1).limit(50))
