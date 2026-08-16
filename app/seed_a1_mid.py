"""Auto-seed A1 MID test data into MongoDB (used at app startup on Railway)."""
from datetime import datetime, timezone

AUDIO = "/static/audio/a1_mid_listening_full.mp3"
IMG = "/static/images/a1_mid/"

questions = [
    # ============ LISTENING Part 1 (Q1-5): picture MC ============
    {"id": "l_p1", "type": "multiple_group", "section": "listening", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nYou will hear five short recordings. For each question, choose the correct picture.\nYou will hear each conversation twice.",
     "points": 5,
     "items": [
         {"q": "1. Where does the woman have lunch?",
          "option_images": [IMG + "lq1_A.png", IMG + "lq1_B.png", IMG + "lq1_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "2. When does the woman usually have breakfast?",
          "option_images": [IMG + "lq2_A.png", IMG + "lq2_B.png", IMG + "lq2_C.png"],
          "options": ["A", "B", "C"], "answer": 1},
         {"q": "3. What does the man usually have for lunch?",
          "option_images": [IMG + "lq3_A.png", IMG + "lq3_B.png", IMG + "lq3_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "4. What drink does the woman order?",
          "option_images": [IMG + "lq4_A.png", IMG + "lq4_B.png", IMG + "lq4_C.png"],
          "options": ["A", "B", "C"], "answer": 0},
         {"q": "5. Who is Steve's brother?",
          "option_images": [IMG + "lq5_A.png", IMG + "lq5_B.png", IMG + "lq5_C.png"],
          "options": ["A", "B", "C"], "answer": 0},
     ]},

    # ============ LISTENING Part 2 (Q6-10): matching name -> job ============
    {"id": "l_p2", "type": "matching", "section": "listening", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nListen to Joe talking to Claire about his family. Which job does each person do?\nFor each question 6-10, write a letter A-G next to it.\nYou will hear the conversation twice.",
     "points": 5,
     "options": ["6. Jane", "7. Becky", "8. Sam", "9. Daniel", "10. Mary"],
     "items": ["A Doctor", "B Businessman", "C Student", "D Shop assistant",
               "E Hotel receptionist", "F Waitress", "G Teacher"],
     "answer": [3, 6, 4, 2, 5]},

    # ============ LISTENING Part 3 (Q11-15): MC ============
    {"id": "l_p3", "type": "multiple_group", "section": "listening", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nYou will hear an interview with a woman called Lisa Galvani talking about going on holiday to another country for twelve weeks.\nFor each question, choose the correct answer.\nYou will hear the conversation twice.",
     "points": 5,
     "items": [
         {"q": "11. Where does Lisa work?",
          "options": ["in a factory", "in an office", "at home"], "answer": 2},
         {"q": "12. Where does Lisa want to go now?",
          "options": ["China", "Mexico", "Turkey"], "answer": 0},
         {"q": "13. Who can go with Lisa?",
          "options": ["her husband", "her sister", "her brother"], "answer": 1},
         {"q": "14. What does Lisa need to buy?",
          "options": ["a book", "a ticket", "a phone"], "answer": 2},
         {"q": "15. What does Lisa want to write a blog about?",
          "options": ["interesting people", "big museums", "beautiful beaches"], "answer": 1},
     ]},

    # ============ LISTENING Part 4 (Q16-20): gap-fill ============
    {"id": "l_p4", "type": "writing", "section": "listening", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nYou will hear a woman telling her mother about her news.\nFor each question, write the correct answer in the gap.\nYou will hear the recording twice.",
     "title": "Fatima's hotel",
     "passage": "The hotel address: 26 (16) ________ Road\n\nThe hotel doesn't have a: (17) ________\n\nThe hotel phone number is: (18) ________\n\nThe receptionist is from: (19) ________\n\nA good time to phone is: (20) ________",
     "gap_items": ["Station", "swimming pool", "82-97-74", "Brazil", "7"],
     "gap_labels": ["16", "17", "18", "19", "20"],
     "points": 5},

    # ============ READING Part 1 (Q1-5): matching sentence -> place ============
    {"id": "r_p1", "type": "matching", "section": "reading", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nRead the sentences.\nFor each question 1-5, write a letter A-G next to it.",
     "points": 5,
     "options": [
         "1. I have breakfast here every day before I go to school.",
         "2. I want to go shopping, but first I need to get some money.",
         "3. People usually sit here and look at the beautiful flowers and trees.",
         "4. There are a lot of interesting old things to look at.",
         "5. We usually go there at the weekend to watch something.",
     ],
     "items": ["A Museum", "B Shop", "C Cinema", "D Classroom", "E Bank", "F Cafe", "G Park"],
     "answer": [5, 4, 6, 0, 2]},

    # ============ READING Part 2 (Q6-10): MC Martin's daily routine ============
    {"id": "r_p2", "type": "multiple_group", "section": "reading", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nRead the sentences about Martin's daily routine, and choose the correct answer for each gap.",
     "points": 5,
     "items": [
         {"q": "6. Martin ........ in a flat in a big city and works in a bank.",
          "options": ["lives", "goes", "studies"], "answer": 0},
         {"q": "7. When Martin is on the train, he likes to read a ........ .",
          "options": ["phone", "wi-fi", "newspaper"], "answer": 2},
         {"q": "8. Martin ........ work at 5pm.",
          "options": ["gets up", "goes", "finishes"], "answer": 2},
         {"q": "9. In the evening, Martin usually goes home to have ........ with his mother.",
          "options": ["breakfast", "dinner", "lunch"], "answer": 1},
         {"q": "10. At the weekend, he likes to play football with friends - he is very ........ then.",
          "options": ["happy", "right", "easy"], "answer": 0},
     ]},

    # ============ READING Part 3 (Q11-15): MC A Teacher's Life ============
    {"id": "r_p3", "type": "multiple_group", "section": "reading", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nRead the text about Janet, a teacher, and the questions below.\nFor each question, circle the correct letter A, B, or C.",
     "title": "A Teacher's Life",
     "passage": "I'm a teacher and I love my job. It's not an easy job - there are always problems, but it's never boring. I usually arrive at school at 7:30, and so I get up at 6:30. There is a lot of work to do before the students arrive at 8:30.\n\nI need to get there early because sometimes parents come to talk to me before school starts. There are 30 children in my class. When they come to school, they sometimes talk to me about why they aren't happy. I feel sad then, but they also talk about good things and sometimes they are very funny.\n\nI start teaching the morning lessons at 9:00. We usually use textbooks to teach children, but we sometimes use computers because the children have fun using them.\n\nLunch time starts at 11:55. It's a busy time for the teachers. The children eat lunch together but the teachers stay in their classrooms eating and working because we need to think about the afternoon lessons. We don't usually have time to eat a big lunch, just fruit and a sandwich.\n\nIn the afternoon, the children are tired and they don't want to learn maths. We play games or we go to the park. They are happy with their friends.\n\nSchool finishes at 3:15 and the children go home. Teachers stay to work and I never go home before 5:00; usually it's 7:00. At the end of the day I'm tired but happy.",
     "points": 5,
     "items": [
         {"q": "11. Janet gets to work at",
          "options": ["6.30.", "7.30.", "8.30."], "answer": 1},
         {"q": "12. Janet is not happy when",
          "options": ["there are many children in her class.", "the children's parents talk to her.", "the children have problems."], "answer": 2},
         {"q": "13. At lunchtime the teachers",
          "options": ["don't have much time.", "don't work.", "eat a lot of food."], "answer": 0},
         {"q": "14. In the afternoon the children",
          "options": ["don't want to study.", "go to sleep.", "don't play with their friends."], "answer": 0},
         {"q": "15. Janet's day usually finishes at",
          "options": ["a quarter past three.", "five o'clock.", "seven o'clock."], "answer": 2},
     ]},

    # ============ READING Part 4 (Q16-20): gap-fill MC Bristol ============
    {"id": "r_p4", "type": "multiple_group", "section": "reading", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nRead the text about the city of Bristol in the UK and choose the correct answer for each gap.",
     "inline_gaps": True,
     "passage": "Bristol is a beautiful small city in the UK, and there are many things to see and do there. It has a lot of small shops - they sell local things. The local people (16) ________ want to shop in the big supermarkets because they (17) ________ like to spend money to help (18) ________ local businesses. (19) ________ a very nice city with lots of trees, and the parks and river are nice places to go for a walk. In many places the (20) ________ are also very old and beautiful.",
     "points": 5,
     "items": [
         {"q": "16.", "options": ["isn't", "aren't", "don't"], "answer": 2},
         {"q": "17.", "options": ["never", "usually", "every day"], "answer": 1},
         {"q": "18.", "options": ["their", "his", "our"], "answer": 0},
         {"q": "19.", "options": ["He's", "They're", "It's"], "answer": 2},
         {"q": "20.", "options": ["house", "houses", "house's"], "answer": 1},
     ]},

    # ============ READING Part 5 (Q21-25): open cloze gap-fill ============
    {"id": "r_p5", "type": "writing", "section": "reading", "part": 5, "start_num": 21,
     "instruction": "Part 5. Questions 21-25.\nRead the text. Think of the word which best fits each gap.\nWrite ONE word for each gap.",
     "title": "Dear Phil",
     "passage": "Dear Phil,\nHi, how are you? I'm at a language school in Italy now. There (21) ________ lots of students in my class - all from different countries. (22) ________ aren't any other English people - only me. My teacher's name is Sara. She's very good. The lessons are interesting but they're sometimes difficult. I speak a lot of Italian because she (23) ________ not speak English in class with us. I see Sara every day because she lives near my hotel. I like the food here but Italian people usually (24) ________ dinner in restaurants very late, sometimes at 10 o'clock at night! (25) ________ you like Italian food?\n\nBest wishes,\nCathy",
     "gap_items": ["are", "There", "does", "eat", "Do"],
     "gap_labels": ["21", "22", "23", "24", "25"],
     "points": 5},

    # ============ WRITING ============
    {"id": "w1", "type": "writing", "section": "writing", "start_num": 1,
     "question": "Read the email from your English friend, Marco.\n\nFrom: Marco\nTell me about your school subjects.\n\n• What subjects do you like to study?\n• Which subject is easy for you?\n• Which subject is difficult for you?\n\nWrite an email to Marco and answer the questions.\nWrite at least 50 words.",
     "word_limit": "50", "points": 20},
]

test = {
    "section": "a1_mid",
    "title": "🔰 A1 · MID",
    "icon": "🔰",
    "time_limit": 55,
    "price": 0,
    "original_price": 0,
    "active": True,
    "description": "A1 daraja oraliq imtihoni — Listening + Reading + Writing",
    "audio_parts": [AUDIO, AUDIO, AUDIO, AUDIO],
    "created_at": datetime.now(timezone.utc),
    "questions": questions,
}

def seed_a1_mid(db):
    """Insert or update the A1 MID test document (keeps _id stable so old attempts work)."""
    # Upsert: keep the existing _id so old attempts still reference a valid test
    db.tests.update_one(
        {"section": "a1_mid"},
        {"$set": test},
        upsert=True,
    )
    return len(test["questions"])
