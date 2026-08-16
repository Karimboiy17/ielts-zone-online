"""Auto-seed A2 END test data into MongoDB (used at app startup on Railway)."""
from datetime import datetime, timezone

AUDIO = "/static/audio/a2_end_listening_full.mp3"
IMG = "/static/images/a2_end/"

questions = [
    # ============ LISTENING Part 1 (Q1-5): pictures ============
    {"id": "l_p1", "type": "multiple_group", "section": "listening", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nYou will hear five short conversations. You will hear each conversation twice.\nFor each question put a tick under the right answer.",
     "points": 5,
     "items": [
         {"q": "1. What will they eat for dinner this evening?", "option_images": [IMG + "lq1_A.png", IMG + "lq1_B.png", IMG + "lq1_C.png"],
          "options": ["A", "B", "C"], "answer": 1},
         {"q": "2. What time is it?", "option_images": [IMG + "lq2_A.png", IMG + "lq2_B.png", IMG + "lq2_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "3. What's Michelle going to read?", "option_images": [IMG + "lq3_A.png", IMG + "lq3_B.png", IMG + "lq3_C.png"],
          "options": ["A", "B", "C"], "answer": 1},
         {"q": "4. How much did the tickets cost?", "option_images": [IMG + "lq4_A.png", IMG + "lq4_B.png", IMG + "lq4_C.png"],
          "options": ["A", "B", "C"], "answer": 1},
         {"q": "5. Where is the chemist's?", "option_images": [IMG + "lq5_A.png", IMG + "lq5_B.png", IMG + "lq5_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
     ]},

    # ============ LISTENING Part 2 (Q6-10): matching days/weather ============
    {"id": "l_p2", "type": "matching", "section": "listening", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nListen to Pete talking to a friend about his holiday. What was the weather like each day?\nFor questions 6-10, write a letter A-H next to each day.\nYou will hear the conversation twice.",
     "events": [
         "A cloud", "B cold", "C fog", "D rain",
         "E snow", "F sun", "G warm", "H wind",
     ],
     "options": [
         "6. Tuesday", "7. Wednesday", "8. Thursday",
         "9. Friday", "10. Saturday",
     ],
     "items": ["A cloud", "B cold", "C fog", "D rain", "E snow", "F sun", "G warm", "H wind"],
     "answer": [7, 5, 0, 3, 6],  # Q6=H Q7=F Q8=A Q9=D Q10=G
     "points": 5},

    # ============ LISTENING Part 3 (Q11-15): MC ============
    {"id": "l_p3", "type": "multiple_group", "section": "listening", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nListen to Mrs. Lee talking to her secretary about her business trip.\nFor questions 11-15, tick A, B or C.\nYou will hear the conversation twice.",
     "points": 5,
     "items": [
         {"q": "11. Mrs. Lee's plane goes at", "options": ["8 a.m.", "10 a.m.", "11 a.m."], "answer": 1},
         {"q": "12. She is going to", "options": ["Amsterdam.", "Frankfurt.", "London."], "answer": 2},
         {"q": "13. First, she will go to", "options": ["a factory.", "an office.", "a hotel."], "answer": 0},
         {"q": "14. She will have dinner in", "options": ["a restaurant.", "her hotel.", "someone's house."], "answer": 0},
         {"q": "15. The next morning, she will travel by", "options": ["plane.", "train.", "car."], "answer": 1},
     ]},

    # ============ LISTENING Part 4 (Q16-20): gap-fill form ============
    {"id": "l_p4", "type": "writing", "section": "listening", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nYou will hear Kate and Jeremy talking about a party.\nListen and complete questions 16-20.\nYou will hear the conversation twice.",
     "title": "Kate's Birthday Party",
     "passage": "Kate will be: 17 years old\nDay: (16) ________\nTime: (17) ________\nPlace: (18) ________\nAddress: (19) ________ Street\nBring some: (20) ________",
     "gap_items": ["FRIDAY", "8:30", "LONDON HOTEL", "SHINDY", "PENCILS"],
     "gap_labels": ["16", "17", "18", "19", "20"],
     "points": 5},

    # ============ READING Part 1 (Q1-5): notices A-H ============
    {"id": "r_p1", "type": "matching", "section": "reading", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nWhich notice (A-H) says this (1-5)?\nFor questions 1-5, mark the correct letter A-H on the answer sheet.",
     "events": [
         "A SUMMER SALE — LOW PRICES IN ALL DEPARTMENTS", "B FIRE DOOR — KEEP CLOSED",
         "C LIFT NOT WORKING", "D TOY SHOP NOW OPEN",
         "E BUY NOW PAY NEXT YEAR!", "F Keep this nightdress away from fire!",
         "G We do not take cheques or credit cards.", "H Under 12s HALF PRICE",
     ],
     "options": [
         "1. Children pay less than adults here.",
         "2. Be careful because this will burn.",
         "3. We don't want any money yet.",
         "4. Things are cheaper here.",
         "5. You must pay with cash.",
     ],
     "items": ["A SUMMER SALE", "B FIRE DOOR — KEEP CLOSED", "C LIFT NOT WORKING",
               "D TOY SHOP NOW OPEN", "E BUY NOW PAY NEXT YEAR!",
               "F Keep this nightdress away from fire!", "G No cheques or credit cards.",
               "H Under 12s HALF PRICE"],
     "answer": [7, 5, 4, 0, 6],  # Q1=H Q2=F Q3=E Q4=A Q5=G
     "points": 5},

    # ============ READING Part 2 (Q6-10): MC ============
    {"id": "r_p2", "type": "multiple_group", "section": "reading", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nRead the sentences about the swimming pool and choose the correct answer for each gap.",
     "points": 5,
     "items": [
         {"q": "6. Everyone must ________ a shower before they go in the water.", "options": ["do", "make", "take"], "answer": 2},
         {"q": "7. There are special changing rooms for ________ with young children.", "options": ["brothers", "parents", "cousins"], "answer": 1},
         {"q": "8. Please ________ to take a towel with you to the pool.", "options": ["know", "understand", "remember"], "answer": 2},
         {"q": "9. If you are ________, you can get a drink in the snack bar upstairs.", "options": ["dirty", "thirsty", "wet"], "answer": 1},
         {"q": "10. In the afternoons, there are swimming classes for children of all ________.", "options": ["ages", "lessons", "pupils"], "answer": 0},
     ]},

    # ============ READING Part 3 (Q11-15): MC ============
    {"id": "r_p3", "type": "multiple_group", "section": "reading", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nRead the article about Rebecca Stevens and answer the questions.\nFor each question mark A, B or C on the answer sheet.",
     "title": "REBECCA STEVENS",
     "passage": "Rebecca Stevens was the first woman to climb Mount Everest. Before she went up the highest mountain in the world, she was a journalist and lived in a small flat in south London.\n\nIn 1993, Rebecca left her job and her family and travelled to Asia with some other climbers. She found that life on Everest is hard. 'You must carry everything on your back,' she explained, 'so you can only take things that you will need. You can't wash on the mountain, and in the end, I didn't even take a toothbrush. I am usually a clean person but there is no water, only snow. Water is very heavy, so you only take enough to drink.'\n\nWhen Rebecca reached the top of Mount Everest on May 17, 1993, it was the best moment of her life. Suddenly she became famous. Now, she has written a book about the trip and people often ask her to talk about it. She has a new job too, on a science programme on television. Rebecca is well-known today and she has more money, but she still lives in the little flat in south London among her pictures and books about mountains!",
     "points": 5,
     "items": [
         {"q": "11. Before Rebecca climbed Everest, she worked for", "options": ["a bookshop.", "a newspaper.", "a travel agent."], "answer": 1},
         {"q": "12. Rebecca went to Everest", "options": ["with her family.", "with a climbing group.", "without anyone."], "answer": 1},
         {"q": "13. Rebecca didn't take much luggage because she", "options": ["didn't have many things.", "had a bad back.", "had to carry it herself."], "answer": 2},
         {"q": "14. Rebecca didn't wash on Everest because", "options": ["it was too cold.", "there was not enough water.", "she is a dirty person."], "answer": 1},
         {"q": "15. Rebecca carried water for", "options": ["drinking.", "cooking.", "cleaning her teeth."], "answer": 0},
     ]},

    # ============ READING Part 4 (Q16-20): gap-fill MC ============
    {"id": "r_p4", "type": "multiple_group", "section": "reading", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nRead the article about a working holiday and answer the questions.\nFor each question mark A, B or C on the answer sheet.",
     "title": "The Ruwenzori Mountains",
     "inline_gaps": True,
     "passage": "Mary Daniels is a student in England. This year she had a very interesting summer holiday. She travelled (16) ________ fifteen other people to the Ruwenzori Mountains in Africa. They went there to help make a road (17) ________ a forest between two big towns.\n\n'It was very difficult (18) ________ there was no water to drink and no shops where we could buy food,' said Mary. 'It was also very cold and wet in the mountains. It is one of the wettest places in the world.'\n\nMary stayed in the mountains for six weeks. It was hard work, but she says it was the (19) ________ thing she has ever (20) ________. She is hoping to return next year to do some more work there.",
     "points": 5,
     "items": [
         {"q": "16. She travelled (16) ________ fifteen other people.", "options": ["to", "with", "by"], "answer": 1},
         {"q": "17. make a road (17) ________ a forest.", "options": ["through", "on", "among"], "answer": 0},
         {"q": "18. It was very difficult (18) ________ there was no water.", "options": ["so", "because", "why"], "answer": 1},
         {"q": "19. it was the (19) ________ thing she has ever", "options": ["good", "best", "better"], "answer": 1},
         {"q": "20. thing she has ever (20) ________.", "options": ["did", "do", "done"], "answer": 2},
     ]},

    # ============ READING Part 5 (Q21-25): gap-fill ONE WORD ============
    {"id": "r_p5", "type": "writing", "section": "reading", "part": 5, "start_num": 21,
     "instruction": "Part 5. Questions 21-25.\nRead the text. Think of the word which fits each gap. Write ONE word for each gap.",
     "title": "Two letters",
     "passage": "Dear Sir,\n\nI (Example: read) your advertisement for English courses (21) ________ the newspaper. I would (22) ________ to have some more information.\nHow (23) ________ does a course cost? Also, (24) ________ long is each course and when does the next course start?\n\nYours,\nMaria Gonzalez\n\nDear Ms. Gonzalez,\n\nThank (25) ________ for your letter. Our next course starts in three weeks, Monday, 9 May. This is a 6-week course, and it costs £150. If you prefer to begin in June, we have a 10-week course for £200. I hope this is the information you want.\n\nYours,\nDavid May",
     "gap_items": ["IN", "LIKE", "MUCH", "HOW", "YOU"],
     "gap_labels": ["21", "22", "23", "24", "25"],
     "points": 5},

    # ============ WRITING ============
    {"id": "w1", "type": "writing", "section": "writing", "start_num": 1,
     "question": "Write an email to a classmate in your English class. Invite them to your birthday party.\n\nInclude:\n• the day and time of the party\n• the place\n• what you will do at the party (games, food, music, etc.)\n• ask if they can come\n\nWrite at least 50 words.",
     "word_limit": "50", "points": 20},
]

test = {
    "section": "a2_end",
    "title": "A2 · END",
    "icon": "📘",
    "time_limit": 55,
    "price": 0,
    "original_price": 0,
    "active": True,
    "description": "A2 daraja yakuniy imtihoni — Listening + Reading + Writing",
    "audio_parts": [AUDIO, AUDIO, AUDIO, AUDIO],
    "created_at": datetime.now(timezone.utc),
    "questions": questions,
}

def seed_a2_end(db):
    """Insert or update the A2 END test document (keeps _id stable)."""
    db.tests.update_one({"section": "a2_end"}, {"$set": test}, upsert=True)
    return len(test["questions"])
