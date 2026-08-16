"""Auto-seed A2 MID test data into MongoDB (used at app startup on Railway)."""
from datetime import datetime, timezone

AUDIO = "/static/audio/a2_mid_listening_full.mp3"
IMG = "/static/images/a2_mid/"

questions = [
    # ============ LISTENING Part 1 (Q1-5): pictures ============
    {"id": "l_p1", "type": "multiple_group", "section": "listening", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nYou will hear five short conversations. For questions 1-5, put a tick under the right answer.\nYou will hear each conversation twice.",
     "points": 5,
     "items": [
         {"q": "1. Where's the sports centre?", "option_images": [IMG + "lq1_A.png", IMG + "lq1_B.png", IMG + "lq1_C.png"],
          "options": ["A", "B", "C"], "answer": 0},
         {"q": "2. How much petrol does the woman want?", "option_images": [IMG + "lq2_A.png", IMG + "lq2_B.png", IMG + "lq2_C.png"],
          "options": ["A", "B", "C"], "answer": 1},
         {"q": "3. Which table do they buy?", "option_images": [IMG + "lq3_A.png", IMG + "lq3_B.png", IMG + "lq3_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "4. What time does the class start?", "option_images": [IMG + "lq4_A.png", IMG + "lq4_B.png", IMG + "lq4_C.png"],
          "options": ["A", "B", "C"], "answer": 0},
         {"q": "5. What was the weather like on Emma's holiday?", "option_images": [IMG + "lq5_A.png", IMG + "lq5_B.png", IMG + "lq5_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
     ]},

    # ============ LISTENING Part 2 (Q6-10): matching A-H ============
    {"id": "l_p2", "type": "matching", "section": "listening", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nListen to Philip talking to his mother about his son, Simon. What is Simon going to do on Saturday and Sunday?\nFor questions 6-10, write a letter A-H next to each question.\nYou will hear the conversation twice.",
     "events": [
         "A bicycle ride", "B football match", "C judo class", "D party",
         "E swimming", "F the cinema", "G the park", "H watching television",
     ],
     "options": [
         "6. Saturday afternoon", "7. Saturday evening", "8. Sunday morning",
         "9. Sunday afternoon", "10. Sunday evening",
     ],
     "items": ["A bicycle ride", "B football match", "C judo class", "D party",
               "E swimming", "F the cinema", "G the park", "H watching television"],
     "answer": [1, 3, 0, 6, 7],  # Q6=B Q7=D Q8=A Q9=G Q10=H
     "points": 5},

    # ============ LISTENING Part 3 (Q11-15): MC ============
    {"id": "l_p3", "type": "multiple_group", "section": "listening", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nListen to a woman talking to a policeman. For questions 11-15, tick A, B or C.\nYou will hear the conversation twice.",
     "points": 5,
     "items": [
         {"q": "11. How much money was in the bag?", "options": ["20", "40", "50"], "answer": 0},
         {"q": "12. What else was in the bag?", "options": ["credit card", "driving license", "gloves"], "answer": 2},
         {"q": "13. The bag was", "options": ["old.", "expensive.", "big."], "answer": 0},
         {"q": "14. What time did the woman lose the bag?", "options": ["9.30", "10.00", "10.30"], "answer": 1},
         {"q": "15. The policeman will telephone her in the", "options": ["morning", "afternoon", "evening"], "answer": 0},
     ]},

    # ============ LISTENING Part 4 (Q16-20): gap-fill form ============
    {"id": "l_p4", "type": "writing", "section": "listening", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nYou will hear a conversation about a flat for rent.\nListen and complete questions 16-20.",
     "title": "LONFLATS AGENCY — Flat for rent in: Putney",
     "passage": "Number of bedrooms: (16) ________\nCost: (17) ________ a month\nAddress: 27 (18) ________ Street\nWhen see flat? Tuesday at (19) ________\nFree from: (20) ________",
     "gap_items": ["TWO", "440", "EARSLEY", "5:30", "MARCH"],
     "gap_labels": ["16", "17", "18", "19", "20"],
     "points": 5},

    # ============ READING Part 1 (Q1-5): notices A-H ============
    {"id": "r_p1", "type": "matching", "section": "reading", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nWhich notice (A-H) says this (1-5)?\nFor questions 1-5, mark the correct letter A-H on the answer sheet.",
     "events": [
         "A KEEP IN FRIDGE", "B Door locked at midnight — ask for key before going out",
         "C SOUP AND HOT PIES ONLY", "D TICKETS FOR OASIS CONCERT ON SALE HERE — ALL THIS WEEK",
         "E BUY 5 GET 1 FREE", "F NO ANIMALS IN RESTAURANT",
         "G ALL TICKETS SOLD", "H USE BY 19 JULY",
     ],
     "options": [
         "1. These are cheaper if you buy several of them.",
         "2. You can't get many different meals out here.",
         "3. Put this in a cold place.",
         "4. You are too late to get a seat for this show.",
         "5. This place is not open all night.",
     ],
     "items": ["A KEEP IN FRIDGE", "B Door locked at midnight", "C SOUP AND HOT PIES ONLY",
               "D TICKETS FOR OASIS CONCERT ON SALE HERE", "E BUY 5 GET 1 FREE",
               "F NO ANIMALS IN RESTAURANT", "G ALL TICKETS SOLD", "H USE BY 19 JULY"],
     "answer": [4, 2, 0, 6, 1],  # Q1=E Q2=C Q3=A Q4=G Q5=B
     "points": 5},

    # ============ READING Part 2 (Q6-10): MC ============
    {"id": "r_p2", "type": "multiple_group", "section": "reading", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nRead the sentences (6-10) about cooking. Choose the best word (A, B or C) for each space.",
     "points": 5,
     "items": [
         {"q": "6. She ________ some fruit and vegetables from the market.", "options": ["bought", "kept", "grew"], "answer": 0},
         {"q": "7. She cut up some meat and onions and fried them in a pan on the ________.", "options": ["cooker", "cupboard", "fridge"], "answer": 0},
         {"q": "8. There was a big ________ of salad to eat afterwards.", "options": ["bottle", "bowl", "spoon"], "answer": 1},
         {"q": "9. When everything was ________, they all sat down at the table.", "options": ["real", "round", "ready"], "answer": 2},
         {"q": "10. After dinner, Claudia's parents ________ her to wash up.", "options": ["practiced", "agreed", "helped"], "answer": 2},
     ]},

    # ============ READING Part 3 (Q11-15): Right/Wrong/Doesn't say ============
    {"id": "r_p3", "type": "multiple_group", "section": "reading", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nRead the article about Canada Geese.\nFor each question mark A, B or C on the answer sheet.",
     "title": "Canada Geese",
     "passage": "Canada Geese are large blue and white birds. When autumn arrives, they must fly south where the weather is warmer. The winters are so cold in Canada that the birds die if they stay there.\n\nLast spring, Bill Lishman found sixteen young Canada Geese on his farm. They had lost their parents. Bill thought, 'These young birds won't know what to do in the autumn.' Bill had a small plane, and he decided to teach the birds to follow him. All through the summer, he went on short trips in his plane, and the young geese flew after him.\n\nWhen the cold weather arrived in autumn, Bill flew to Virginia in the United States, 600 miles south of his home in Canada. The geese followed him all the way. Bill left the geese in Virginia and he returned home.\n\nThis spring, Bill was waiting for the birds to come back. They didn't arrive, so Bill flew to Virginia to get them. He looked for them for two weeks, but he couldn't find them. When he arrived back home, Bill found the geese waiting for him. They had found their way home without him!",
     "points": 5,
     "items": [
         {"q": "11. Bill Lishman is a farmer.", "options": ["Right", "Wrong", "Doesn't say"], "answer": 0},
         {"q": "12. Bill lives with his parents.", "options": ["Right", "Wrong", "Doesn't say"], "answer": 2},
         {"q": "13. Bill carried the geese in his plane.", "options": ["Right", "Wrong", "Doesn't say"], "answer": 1},
         {"q": "14. This was Bill's first visit to Virginia.", "options": ["Right", "Wrong", "Doesn't say"], "answer": 2},
         {"q": "15. Bill wanted the geese to stay at his home for the winter.", "options": ["Right", "Wrong", "Doesn't say"], "answer": 1},
     ]},

    # ============ READING Part 4 (Q16-20): gap-fill MC ============
    {"id": "r_p4", "type": "multiple_group", "section": "reading", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nRead the article about air travel.\nChoose the correct answer for each gap.",
     "title": "A HISTORY OF AIR TRAVEL",
     "inline_gaps": True,
     "passage": "In 1783, two French brothers built the first balloon to take people into the air. One hundred and twenty years later, in 1903, the Wright brothers built the first plane with an engine and (16) ________ in it. This was (17) ________ the United States. Then, in 1918, the US Post Office began the first airmail service.\n\nAeroplanes changed a (18) ________ in the next thirty years. Then, in the 1950s, aeroplanes became much faster because they had jet engines.\n\nIn 1976, Concorde was built in the UK and France. It is the fastest passenger plane in the world and it (19) ________ fly at 2500 kilometers an hour, so the journey from London to New York is only four hours.\n\nToday, millions of people travel (20) ________ aeroplane, and it is difficult to think of a world without them.",
     "points": 5,
     "items": [
         {"q": "16. ________ in it.", "options": ["fly", "flown", "flew"], "answer": 2},
         {"q": "17. This was ________ the United States.", "options": ["in", "at", "through"], "answer": 0},
         {"q": "18. Aeroplanes changed a ________ in the next thirty years.", "options": ["lot", "many", "few"], "answer": 0},
         {"q": "19. It ________ fly at 2500 kilometers an hour.", "options": ["must", "should", "can"], "answer": 2},
         {"q": "20. Today, millions of people travel ________ aeroplane.", "options": ["with", "on", "by"], "answer": 2},
     ]},

    # ============ READING Part 5 (Q21-25): gap-fill ONE WORD ============
    {"id": "r_p5", "type": "writing", "section": "reading", "part": 5, "start_num": 21,
     "instruction": "Part 5. Questions 21-25.\nComplete these letters.\nWrite ONE word for each space.",
     "title": "Two letters",
     "passage": "Dear Jacqueline,\n\nWould you like to come to the cinema (21) ________ me after school today?\nWe can go to see Pocahontas at the ABC cinema. The film starts (22) ________ 6 o'clock.\nShall (23) ________ meet outside the cinema?\n\nLove,\nIsabella\n\nDear Isabella,\n\nI am very sorry, but I can't go to the cinema (24) ________ evening.\nMy mother has (25) ________ work, and I am going to cook dinner.\nWhy don't you ask Karen to go? I hope you like the film.\nYou can tell me about it tomorrow.\n\nLove,\nJacqueline",
     "gap_items": ["WITH", "AT", "WE", "THIS", "GOT"],
     "gap_labels": ["21", "22", "23", "24", "25"],
     "points": 5},

    # ============ WRITING ============
    {"id": "w1", "type": "writing", "section": "writing", "start_num": 1,
     "question": "Your friend sent you an email talking about their favourite food.\n\nWrite a reply.\n\nIn your email:\n• thank your friend for the message\n• say what food you like\n• say when and where you eat it\n• ask your friend a question about food\n\nWrite about 50 words.",
     "word_limit": "50", "points": 20},
]

test = {
    "section": "a2_mid",
    "title": "A2 · MID",
    "icon": "📘",
    "time_limit": 55,
    "price": 0,
    "original_price": 0,
    "active": True,
    "description": "A2 daraja oraliq imtihoni — Listening + Reading + Writing",
    "audio_parts": [AUDIO, AUDIO, AUDIO, AUDIO],
    "created_at": datetime.now(timezone.utc),
    "questions": questions,
}

def seed_a2_mid(db):
    """Insert or update the A2 MID test document (keeps _id stable)."""
    db.tests.update_one({"section": "a2_mid"}, {"$set": test}, upsert=True)
    return len(test["questions"])
