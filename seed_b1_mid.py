#!/usr/bin/env python3
"""Seed B1 MID (8) exam into IELTS ZONE online platform."""
import sys, os

BASE = "/home/karimboy/projects/ielts-zone-online"
SITE = os.path.join(BASE, ".venv", "lib", "python3.11", "site-packages")
sys.path.insert(0, BASE)
sys.path.insert(0, SITE)

from pymongo import MongoClient
from datetime import datetime, timezone

_uri = os.getenv("MONGO_URI") or os.getenv("MONGO_URL") or "mongodb://localhost:27017/ielts_zone"
client = MongoClient(_uri)
_db_name = os.getenv("MONGO_DB_NAME", "ielts_zone")
try:
    _path = _uri.split("//", 1)[1].split("/", 1)
    if len(_path) > 1 and _path[1]:
        _db_name = _path[1].split("?")[0]
except Exception:
    pass
db = client[_db_name]

AUDIO = "/static/audio/b1mid8_listening_full.mp3"
IMG = "/static/images/b1mid8/"

questions = [
    # ============ LISTENING Part 1 (Q1-5): pictures ============
    {"id": "l_p1", "type": "multiple_group", "section": "listening", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nYou will hear five short recordings. For each question, choose the correct picture.\nYou will hear each recording twice.",
     "points": 5,
     "items": [
         {"q": "1. What did John take with him on holiday?",
          "option_images": [IMG + "p2_img11.png", IMG + "p2_img7.png", IMG + "p2_img9.png"],
          "options": ["A", "B", "C"], "answer": 0},
         {"q": "2. Which accessories were most popular last week?",
          "option_images": [IMG + "p2_img0.png", IMG + "p2_img13.png", IMG + "p2_img2.png"],
          "options": ["A", "B", "C"], "answer": 0},
         {"q": "3. What job does John hope to do when he finishes studying?",
          "option_images": [IMG + "p2_img3.png", IMG + "p2_img4.png", IMG + "p2_img5.png"],
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "4. What travel problem particularly annoyed the film director?",
          "option_images": [IMG + "p2_img6.png", IMG + "p2_img8.png", IMG + "p2_img10.png"],
          "options": ["A", "B", "C"], "answer": 0},
         {"q": "5. What does Ellie decide to do?",
          "option_images": [IMG + "p2_img12.png", IMG + "p2_img14.png", IMG + "p2_img1.png"],
          "options": ["A", "B", "C"], "answer": 2},
     ]},

    # ============ LISTENING Part 2 (Q6-10): gap-fill ============
    {"id": "l_p2", "type": "writing", "section": "listening", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nYou will hear a man on the radio talking about his amazing daily journey to work.\nFor each question, write the correct answer in the gap.",
     "title": "Peter's Journey to Work",
     "passage": "Peter lives in York and travels to work in (6) ________.\nPeter's job is a (7) ________.\nPeter's day starts at (8) ________.\n\nDisadvantages:\n• Travel costs: up to £15 000 per year\n• Getting tired and (9) ________ problems\n\nAdvantages:\n• Time to (10) ________ for the next day\n• Can listen to audiobooks",
     "gap_items": ["London", "Designer", "3:30 a.m", "Traffic", "Plan"],
     "gap_labels": ["6", "7", "8", "9", "10"],
     "points": 5},

    # ============ LISTENING Part 3 (Q11-15): MC ============
    {"id": "l_p3", "type": "multiple_group", "section": "listening", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nYou will hear a radio interview with Fiona Baker, an author.\nFor each question, choose the correct answer.",
     "points": 5,
     "items": [
         {"q": "11. Fiona became an author because",
          "options": ["she wanted to as a child.", "her parents advised her to.", "she disliked her teaching career."],
          "answer": 0},
         {"q": "12. Fiona felt most Russian when",
          "options": ["she read Russian books.", "she ate her mother's food.", "she heard her uncle's stories."],
          "answer": 1},
         {"q": "13. Fiona likes to work in a room in her garden because",
          "options": ["she likes to be close to nature.", "it makes her think of Russia.", "she can be on her own there."],
          "answer": 2},
         {"q": "14. Fiona finds the best time for writing is",
          "options": ["when the weather's cold.", "when the days are longer.", "when it's dark outside."],
          "answer": 1},
         {"q": "15. Fiona thinks a good way to write a novel is to",
          "options": ["start with small ideas.", "work backwards from the end.", "plan all of the chapters first."],
          "answer": 0},
     ]},

    # ============ LISTENING Part 4 (Q16-20): YES/NO ============
    {"id": "l_p4", "type": "multiple_group", "section": "listening", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nYou will hear a conversation between Jane and Phil discussing a project on whether teens should work part-time as well as study.\nDecide if each sentence is correct or incorrect.\nIf it is correct, choose YES. If it is incorrect choose NO.",
     "points": 5,
     "items": [
         {"q": "16. Jane thinks some teens may need a car.",
          "options": ["YES", "NO"], "answer": 0},
         {"q": "17. Phil and Jane agree that teenagers who work always have problems with schoolwork.",
          "options": ["YES", "NO"], "answer": 1},
         {"q": "18. Phil believes that free-time activities are important for teens' futures.",
          "options": ["YES", "NO"], "answer": 0},
         {"q": "19. Phil thinks that most teens should avoid getting a part-time job.",
          "options": ["YES", "NO"], "answer": 1},
         {"q": "20. Jane advises teens to get a summer job rather than work during term-time.",
          "options": ["YES", "NO"], "answer": 1},
     ]},

    # ============ READING Part 1 (Q1-5): notices ============
    {"id": "r_p1", "type": "multiple_group", "section": "reading", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nLook at the text in each question. What does it say?\nFor each question, circle the correct letter A, B, or C.",
     "points": 5,
     "items": [
         {"q": "1. Jane: \"This is the worst holiday I've ever been on. Please contact the travel agent. I really need to get an earlier plane home.\"\n\nWhat does Jane want Mike to do for her?",
          "options": ["take a plane and join her soon", "find out about flights for her", "plan another holiday for her"],
          "answer": 1},
         {"q": "2. \"Gilly, Tina called – she wants to go to the new shopping centre after work tonight. She wants you to go too. Please phone her back before 6 p.m. — Mum\"",
          "options": ["Tina should phone her mother back.", "Tina and Gilly have planned to meet at 6 p.m.", "Tina would like Gilly to go with her."],
          "answer": 2},
         {"q": "3. \"Tom – your colleague Pete called about the trip. Please send him an email with the details of when you're leaving on Saturday. He wants to make sure he'll be at your house on time.\"",
          "options": ["Tom has to make plans for the trip.", "Tom must find out everything for the trip.", "Tom needs to provide information about the trip."],
          "answer": 2},
         {"q": "4. \"TUESDAY ONLY — Remember – show your customer card before you pay to get special offers.\"",
          "options": ["Some people can buy things more cheaply.", "Special prices are available all week.", "The shop will provide customer cards on Tuesday only."],
          "answer": 0},
         {"q": "5. \"Laura, your friend Jess called. She is giving away some vegetables from her garden. Call her later if you want some. You can pick them up tomorrow.\"",
          "options": ["Jess wants Laura to help her with her vegetable garden tomorrow.", "Jess wants Laura to call her tomorrow to buy some vegetables.", "Jess wants Laura to come round tomorrow if she'd like some vegetables."],
          "answer": 2},
     ]},

    # ============ READING Part 2 (Q6-10): matching people to activities ============
    {"id": "r_p2", "type": "matching", "section": "reading", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nThe people below all want to do a local activity.\nOn the opposite page there are eight activities in the local area.\nDecide which activity would be the most suitable for the people below.",
     "points": 5,
     "events": [
         "Friends of Hamley Park — Come along to 'Friends of Hamley Park' for our monthly litter pick. Join our friendly team of adults and children every Sunday to help us keep our lovely local park tidy and something to be proud of. We provide all the tools and equipment you'll need. Just come along on the day and we'll find something for you to do.",
         "Yoga sessions — Yoga sessions with Petra aimed at your level. I know how important it can be for you mums to get out of the house and do some exercise. My fun weekly 'Mum and Child' yoga classes start on Monday 18 June. Buy five sessions and get one free.",
         "Broadchester Park — You are invited to come along for our weekly picnic in Broadchester Park. Open to all, young and old, it's held every Tuesday throughout the summer at 12.00. Please note there will be a charge for food which will be supplied by the café.",
         "Poetry competition — Come and see the winners of this poetry competition. The theme was the natural world and the poets will be performing their work in the beautiful surroundings of Kimberley Park. Entry costs £2. Children under 11 are free.",
         "Storytelling — Storytelling has become popular lately, especially for those who want to tell their story on stage in front of a live audience. Join our one-day event on Wednesday – we'll be looking at how to feel confident and keep your audience interested.",
         "Time to relax — A new six-week yoga course for beginners. Help yourself become more focused, reduce your stress levels, sleep better and improve your mental health. I will be running these courses in the local community centre on Wednesday and Thursday mornings from 11.00 till 12.00. Childcare is available for babies and young children.",
         "The community café — Our community café is looking for young volunteer waiters and waitresses to help us throughout the summer period. You'll learn skills that will be useful when you start your job search. We're looking for anyone who is at least 18 and would like you to be available for at least two days per week.",
         "Creswell Youth Centre — Are you interested in developing your acting skills? Creswell Youth Centre is offering young people aged from 7 to 19 the chance to join us for our next show. No experience is required as we can offer a role to all abilities. You will need to be available at weekends throughout the summer.",
     ],
     "options": [
         "6. Susie has a teenage son who is very interested in acting and wants to learn how to perform on stage. However, due to his other commitments, he is unavailable on Saturdays and Sundays.",
         "7. Gareth is 21 years old and is on summer vacation before returning to university. He is looking for voluntary work that will provide him with experience in working with customers.",
         "8. Marcia wants to take her children to the park one day next week. Her primary goal is to show them the importance of doing something for local people.",
         "9. Ella is a new mother with a three-month-old baby. She is looking for exercise to help her relax. She is free on Monday and Tuesday and also loves getting a bargain.",
         "10. Jacob is looking for somewhere to take his son for lunchtime on any day this week. He specifically wants to go somewhere that is outside to get some fresh air.",
     ],
     "option_images": [IMG + "p7_person6.png", IMG + "p7_person7.png", IMG + "p7_person8.png",
                       IMG + "p7_person9.png", IMG + "p7_person10.png"],
     "items": ["A Friends of Hamley Park", "B Yoga sessions", "C Broadchester Park",
               "D Poetry competition", "E Storytelling", "F Time to relax",
               "G The community café", "H Creswell Youth Centre"],
     "answer": [4, 6, 0, 1, 2]},

    # ============ READING Part 3 (Q11-15): YES/NO Rhossili Bay ============
    {"id": "r_p3", "type": "multiple_group", "section": "reading", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nLook at the sentences below about Rhossili Bay.\nRead the text to decide if each sentence is correct or incorrect.\nIf it is correct, circle Yes. If it is not correct, circle No.",
     "title": "Rhossili Bay",
     "passage": "Travel north-west out of Swansea and before long, you are driving on empty country roads. This is the famous Gower Peninsula, which, in 1956, became the first place in Britain to be called an area of natural beauty. At the end of the Gower Peninsula is Rhossili Bay. Last week it won a prize for being the third best beach in Europe. But it is no tourist beach. There are no bright lights or ice-cream sellers here. In fact, there's nothing for kids to do but enjoy an old-fashioned seaside holiday, having fun on the beach and in the sea. There are not many places left that are like it.\n\nAnd yet the guest book at the Bay Bistro and Café House, one of the few businesses near the bay, is full of recommendations from New Zealanders, and visitors from Brittany, Canada and Belgium. Like the owner, Sue Muddeman, they didn't find this place in the pages of travel magazines, but through hearing about it from others.\n\n\"When I lived in Birmingham and told people I was moving here they already knew of the place,\" Sue says. \"A lot of people come into the café and say they came down here as children. They bring their children back, and then their grandchildren. If people gave me money every time someone said they've been coming here since childhood, I would be a rich woman by now. Sadly, I'm not yet.\"\n\nAt the heart of the beautiful bay, however, are its people. Susan Smale has managed a small souvenir shop in the tiny village of Rhossili for 35 summers and her customers always say the same thing. \"They tell us it's beautiful, but the real difference is the people. They talk to you,\" she says. \"I think that shows how unusual the place is.\"\n\n\"It's never too busy either. The café and the car park might be busy in summer, but in the middle of Rhossili Bay you can always sit on your own, because it's so huge. But there's always more crime when the tourists are around. There are also a few traffic jams and some more rubbish, but tourism is our economy. We've even turned our village hall into a hostel for visitors, which is bringing in a lot of money.\"\n\nNobody, however, would allow Rhossili Bay to lose its character. What makes this place special is the fact it never changes. The only sign of modern life in the bay are some surfers on the ten kilometres of golden sand. But to the north, you can still find walkers and fishermen. The spirit of Rhossili Bay lives on in each and every one of them.",
     "points": 5,
     "items": [
         {"q": "11. Rhossili Bay recently won an international award.",
          "options": ["Yes", "No"], "answer": 0},
         {"q": "12. People usually come to Rhossili Bay after reading about it.",
          "options": ["Yes", "No"], "answer": 1},
         {"q": "13. The people who live in Rhossili Bay are famous for being friendly.",
          "options": ["Yes", "No"], "answer": 0},
         {"q": "14. Susan Smale thinks tourism is bad for Rhossili Bay.",
          "options": ["Yes", "No"], "answer": 1},
         {"q": "15. Rhossili Bay is attractive to different kinds of people.",
          "options": ["Yes", "No"], "answer": 0},
     ]},

    # ============ READING Part 4 (Q16-20): MC Fashion photo project ============
    {"id": "r_p4", "type": "multiple_group", "section": "reading", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nRead the text and questions below.\nFor each question, circle the correct letter A, B, or C.",
     "title": "Fashion photo project",
     "passage": "I used to work as a fashion model, but it's been a long time since I've been part of a fashion photo project. But at 6 a.m. yesterday three cars arrived at the farm where I now live, and a group of 13 people got out.\n\nIt was very busy from the moment they all arrived. The team in charge of clothes had brought so many that they had to work outside. I couldn't believe it! The hair and make-up teams used the big kitchen. They didn't let me in there. \"Don't touch his hair,\" said the photographer. \"That's perfect for the photo. I love it.\"\n\nThe clothes used in fashion photography are all tiny. But to my surprise, most of the clothes weren't too small for me. There was, though, a very tight jacket which I couldn't close. A lady took a pair of scissors and, amazingly, immediately cut straight up the back with one hand while closing the buttons at the front with the other and after just a minute, I was dressed.\n\nThe photographer had got everything ready in a field near the farmhouse. Someone had turned some music up loud and a lot of people were laughing and drinking coffee. It looked like a really fun party.\n\nEverybody was so very busy, the whole time. The photographer's two assistants seemed to be working the hardest. He took hundreds of photos on many different cameras, so they were moving the equipment around all the time.\n\nWe did six completely different scenes in less than three hours. That's Olympic speed. Then they left as quickly as they'd arrived. What a great experience!",
     "points": 5,
     "items": [
         {"q": "16. What is the writer doing in this text?",
          "options": ["telling people about how hard it is to work in fashion", "describing what a fashion photo project can be like", "advising people to have a career in fashion"],
          "answer": 1},
         {"q": "17. The writer was amazed by",
          "options": ["how many people arrived.", "the changes they made to his hair.", "how many things the team had brought."],
          "answer": 2},
         {"q": "18. The writer was surprised when a lady cut his jacket because",
          "options": ["she didn't need to close it.", "it already fit him well.", "she was so fast."],
          "answer": 2},
         {"q": "19. The writer thought there was a party atmosphere because",
          "options": ["people were enjoying themselves.", "people were being lazy.", "people were dancing."],
          "answer": 0},
         {"q": "20. Which of these would make a good headline for the text?",
          "options": ["Man joins the fashion world and becomes famous", "The shocking truth about fashion projects", "The fashion business is so exciting"],
          "answer": 2},
     ]},

    # ============ READING Part 5 (Q21-25): gap-fill MC ============
    {"id": "r_p5", "type": "multiple_group", "section": "reading", "part": 5, "start_num": 21,
     "instruction": "Part 5. Questions 21-25.\nRead the text below and choose the correct answer for each gap.",
     "passage": "When I finished university, I knew I didn't want an office job because I dislike doing the same thing all the time. I love travelling and wanted to (21) ________ as much as possible. So I thought – if I can find a job where I'll be able to see the world, I won't need to get a loan to go travelling. People (22) ________ realise that most flight attendants have degrees and have chosen this career for the advantages it offers.\n\nIt's hard work being on your feet all day. But I enjoy working (23) ________ – my colleagues are really great. And the opportunities to meet new people and learn about different countries are great too. Customers can sometimes be quite (24) ________, but we get training in how to deal with that. I get a good salary and I don't mind packing my (25) ________ every time I fly. I also have plenty of free time to do other things, which I really enjoy.",
     "points": 5,
     "items": [
         {"q": "21. I love travelling and wanted to (21) ________ as much as possible.",
          "options": ["book accommodation", "check into a hotel", "go away"], "answer": 2},
         {"q": "22. People (22) ________ realise that most flight attendants have degrees",
          "options": ["rarely", "especially", "absolutely"], "answer": 0},
         {"q": "23. But I enjoy working (23) ________ – my colleagues are really great.",
          "options": ["long hours", "at weekends", "in a team"], "answer": 2},
         {"q": "24. Customers can sometimes be quite (24) ________",
          "options": ["annoying", "interesting", "disappointing"], "answer": 0},
         {"q": "25. I don't mind packing my (25) ________ every time I fly.",
          "options": ["visa", "accommodation", "suitcase"], "answer": 2},
     ]},

    # ============ WRITING ============
    {"id": "w1", "type": "writing", "section": "writing", "start_num": 1,
     "question": "You borrowed a book from your friend, Emily, and accidentally damaged it.\n\nWrite an email to Emily.\n\nIn your email:\n• Apologize for the damage\n• Explain how it happened\n• Offer to replace or repair the book\n\nWrite at least 100 words.",
     "word_limit": "100", "points": 20},
]

test = {
    "section": "b1_mid",
    "title": "B1 · MID",
    "icon": "📗",
    "time_limit": 55,
    "price": 0,
    "original_price": 0,
    "active": True,
    "description": "B1 daraja oraliq imtihoni — Listening + Reading + Writing",
    "audio_parts": [AUDIO, AUDIO, AUDIO, AUDIO],
    "created_at": datetime.now(timezone.utc),
    "questions": questions,
}

# Upsert: keep _id stable
db.tests.update_one({"section": "b1_mid"}, {"$set": test}, upsert=True)
print(f"✅ B1 MID (8) test yaratildi: {len(questions)} part")
print(f"   Listening: 4, Reading: 5, Writing: 1")
