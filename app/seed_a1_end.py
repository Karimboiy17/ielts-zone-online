"""Auto-seed A1 END test data into MongoDB (used at app startup on Railway).

A1 daraja yakuniy imtihoni — Listening (4 part) + Reading (5 part) + Writing (1 task).
Jami 46 savol. Har bir savol javoblar kaliti bo'yicha to'g'ri index'ga moslangan.

JAVOBLAR KALITI:
LISTENING: Q1=B Q2=C Q3=C Q4=A Q5=C Q6=B Q7=A Q8=E Q9=C Q10=D
           Q11=B Q12=B Q13=B Q14=C Q15=B Q16=MEXICO Q17=50 KM
           Q18=OCTOBER 18th Q19=GRAMMAR Q20=3:30
READING:   Q1=E Q2=A Q3=B Q4=C Q5=D Q6=A Q7=A Q8=A Q9=C Q10=A
           Q11=A Q12=B Q13=C Q14=B Q15=A Q16=B Q17=B Q18=C Q19=A Q20=A
           Q21=WAS Q22=AT Q23=WENT Q24=HAVE Q25=KNOW
"""
from datetime import datetime, timezone

AUDIO = "/static/audio/a1_end_listening_full.mp3"
IMG = "/static/images/a1_end/"

questions = [
    # ============ LISTENING Part 1 (Q1-5): picture MC ============
    {"id": "l_p1", "type": "multiple_group", "section": "listening", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nYou will hear five short conversations. Choose the correct picture (A, B, or C).\nYou will hear each conversation twice.",
     "points": 5,
     "items": [
         {"q": "1. What is the girl doing now?",
          "option_images": [IMG + "lq1_A.png", IMG + "lq1_B.png", IMG + "lq1_C.png"],
          "options": ["A", "B", "C"], "answer": 1},
         {"q": "2. What does the boy want to drink?",
          "option_images": [IMG + "lq2_A.png", IMG + "lq2_B.png", IMG + "lq2_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "3. Where is the dog?",
          "option_images": [IMG + "lq3_A.png", IMG + "lq3_B.png", IMG + "lq3_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "4. What colour is the boy's jacket?",
          "option_images": [IMG + "lq4_A.png", IMG + "lq4_B.png", IMG + "lq4_C.png"],
          "options": ["A", "B", "C"], "answer": 0},
         {"q": "5. What time is the music class?",
          "options": ["4:00", "4:15", "4:30"], "answer": 2},
     ]},

    # ============ LISTENING Part 2 (Q6-10): matching people -> objects ============
    {"id": "l_p2", "type": "matching", "section": "listening", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nYou will hear a boy called Amir talking about what his friends brought to class.\nWrite a letter (A-G) next to each person. You will hear the recording twice.",
     "passage": '<img src="' + IMG + 'l2_objects.png" alt="A-E objects" style="max-width:100%;height:auto;border-radius:8px;">',
     "points": 5,
     "options": ["6. Samira", "7. Leo", "8. Emma", "9. Adam", "10. Mia"],
     "items": ["A", "B", "C", "D", "E"],
     "answer": [1, 0, 4, 2, 3]},

    # ============ LISTENING Part 3 (Q11-15): MC ============
    {"id": "l_p3", "type": "multiple_group", "section": "listening", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nYou will hear a girl called Anna talking about her Sunday.\nChoose the correct answer A, B, or C.",
     "points": 5,
     "items": [
         {"q": "11. What did she do in the morning?",
          "options": ["Watched a film", "Went to the market", "Read a book"], "answer": 1},
         {"q": "12. What did she eat?",
          "options": ["Pasta", "Burger", "Pizza"], "answer": 1},
         {"q": "13. Who was with her?",
          "options": ["Her dad", "Her friend", "Her mum"], "answer": 1},
         {"q": "14. What did she buy?",
          "options": ["a phone", "a bag", "a scarf"], "answer": 2},
         {"q": "15. What time did she go home?",
          "options": ["3:00", "4:00", "5:00"], "answer": 1},
     ]},

    # ============ LISTENING Part 4 (Q16-20): form completion ============
    {"id": "l_p4", "type": "writing", "section": "listening", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nYou will hear a boy called Jonas talking about his English club. Complete the form.\nYou will hear the recording twice.",
     "title": "English Club Details",
     "passage": "Students from:\nChina, (16) ________, and Egypt\n\nKilometres from London:\n(17) ________\n\nMonth club opens:\n(18) ________\n\nMorning subject:\n(19) ________\n\nAfternoon ends at:\n(20) ________",
     "gap_items": ["Mexico", "50 km", "October 18th", "Grammar", "3:30"],
     "gap_labels": ["16", "17", "18", "19", "20"],
     "points": 5},

    # ============ READING Part 1 (Q1-5): matching sentence -> place ============
    {"id": "r_p1", "type": "matching", "section": "reading", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nRead the sentences.\nFor each question, 1-5 write a letter A-G next to it.",
     "passage": '<img src="' + IMG + 'r1_places.png" alt="A-E places" style="max-width:100%;height:auto;border-radius:8px;">',
     "points": 5,
     "options": [
         "1. You go here to borrow books and read quietly.",
         "2. You sleep and keep your clothes here.",
         "3. You watch movies with many people in this place.",
         "4. You wash your hands and brush your teeth here.",
         "5. You go here when you're feeling sick.",
     ],
     "items": ["A", "B", "C", "D", "E"],
     "answer": [4, 0, 1, 2, 3]},

    # ============ READING Part 2 (Q6-10): MC Maya ============
    {"id": "r_p2", "type": "multiple_group", "section": "reading", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nRead the sentences about Maya and choose the correct answer for each gap.",
     "points": 5,
     "items": [
         {"q": "6. Maya usually ........ to school by bus.",
          "options": ["travels", "rides", "drives"], "answer": 0},
         {"q": "7. She ........ lunch at the school cafeteria every day.",
          "options": ["eats", "makes", "brings"], "answer": 0},
         {"q": "8. Maya ........ her homework in the evening.",
          "options": ["does", "plays", "takes"], "answer": 0},
         {"q": "9. On weekends, she likes ........ in the park with her dog.",
          "options": ["walk", "to walking", "walking"], "answer": 2},
         {"q": "10. Maya always ........ to bed at 10 p.m.",
          "options": ["goes", "gets", "sleeps"], "answer": 0},
     ]},

    # ============ READING Part 3 (Q11-15): MC Oli/Zara/Aiden ============
    {"id": "r_p3", "type": "multiple_group", "section": "reading", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nRead the text about three people and the questions below.\nFor each question, circle the correct letter A, B, or C.",
     "title": "Oli, Zara and Aiden",
     "passage": "Oli: I use my phone to take photos of nature. I love walking in the forest and taking pictures of trees, birds, and flowers. I post some of them online and sometimes write short comments. I want to learn how to take better pictures in the future.\n\nZara: I like using social media to chat with friends and share funny videos. I don't post much about myself, but I enjoy reading what other people write. I also follow some famous singers and actors online.\n\nAiden: I don't use social media much, but I like reading the news online. I use my tablet to check headlines and sports updates every evening. Sometimes I watch short news videos too. My parents say it's good to stay informed.",
     "points": 5,
     "items": [
         {"q": "11. Who enjoys sharing pictures of nature?",
          "options": ["Oli", "Zara", "Aiden"], "answer": 0},
         {"q": "12. Who reads about famous people on social media?",
          "options": ["Oli", "Zara", "Aiden"], "answer": 1},
         {"q": "13. Who watches news videos in the evening?",
          "options": ["Oli", "Zara", "Aiden"], "answer": 2},
         {"q": "14. Who doesn't post much but likes reading others' posts?",
          "options": ["Oli", "Zara", "Aiden"], "answer": 1},
         {"q": "15. Who uses their device for learning more about photography?",
          "options": ["Oli", "Zara", "Aiden"], "answer": 0},
     ]},

    # ============ READING Part 4 (Q16-20): inline gap-fill MC ============
    {"id": "r_p4", "type": "multiple_group", "section": "reading", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nRead the text about a trip and choose the correct answer for each gap.",
     "inline_gaps": True,
     "passage": "A Weekend Trip to the Countryside\n\nLast weekend, my friends and I went to a small village in the countryside. We (16) ________ the bus early in the morning and arrived before lunch. It was sunny and warm, so we (17) ________ for a walk in the forest near the village. In the afternoon, we played some games and (18) ________ a picnic by the lake. It was very relaxing! In the evening, we cooked dinner together and sat around a fire. Now we are (19) ________ another trip for next weekend. I hope it will be just as fun. Spending time in nature with friends (20) ________ always a great idea!",
     "points": 5,
     "items": [
         {"q": "16.", "options": ["take", "took", "taken"], "answer": 1},
         {"q": "17.", "options": ["go", "went", "had"], "answer": 1},
         {"q": "18.", "options": ["made", "do", "had"], "answer": 2},
         {"q": "19.", "options": ["planning", "plan", "plans"], "answer": 0},
         {"q": "20.", "options": ["is", "are", "was"], "answer": 0},
     ]},

    # ============ READING Part 5 (Q21-25): open cloze ============
    {"id": "r_p5", "type": "writing", "section": "reading", "part": 5, "start_num": 21,
     "instruction": "Part 5. Questions 21-25.\nRead the text. Think of the word which best fits each gap.\nWrite ONE word for each gap.",
     "title": "Email from Mia",
     "passage": "From: Mia\nTo: Anna\n\nHi Anna!\n\nHow are you doing? I came home from a weekend trip to the mountains. It (21) ________ amazing! We stayed in a small wooden cabin and cooked delicious food together. The weather was great — sunny and warm during the day, but quite cold (22) ________ night. We went hiking and saw some beautiful views. On Sunday, we found a lake and (23) ________ swimming, even though the water was freezing! I really hope you can come with us next time. Do you (24) ________ any plans for the next holiday? We're thinking about going to the beach. Let me (25) ________ what you think!\n\nTalk soon,\nMia",
     "gap_items": ["was", "at", "went", "have", "know"],
     "gap_labels": ["21", "22", "23", "24", "25"],
     "points": 5},

    # ============ WRITING ============
    {"id": "w1", "type": "writing", "section": "writing", "start_num": 1,
     "question": "You are going to the library.\nWrite an email to your English friend, Sophie.\n\nIn your email:\n• Invite Sophie to come with you\n• Say which day you will go\n• Say what books you want to find\n\nWrite at least 50 words.",
     "word_limit": "50", "points": 20},
]

test = {
    "section": "a1_end",
    "title": "🔰 A1 · END",
    "icon": "🔰",
    "time_limit": 55,
    "price": 0,
    "original_price": 0,
    "active": True,
    "description": "A1 daraja yakuniy imtihoni — Listening + Reading + Writing",
    "audio_parts": [AUDIO, AUDIO, AUDIO, AUDIO],
    "created_at": datetime.now(timezone.utc),
    "questions": questions,
}


def seed_a1_end(db):
    """Insert or update the A1 END test document (keeps _id stable so old attempts work)."""
    # Upsert: keep the existing _id so old attempts still reference a valid test
    db.tests.update_one(
        {"section": "a1_end"},
        {"$set": test},
        upsert=True,
    )
    return len(test["questions"])
