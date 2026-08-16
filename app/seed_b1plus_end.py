"""Auto-seed B1+ END test data into MongoDB (used at app startup on Railway)."""
from datetime import datetime, timezone

AUDIO = "/static/audio/b1plus_end_listening_full.mp3"
IMG = "/static/images/b1plus_end/"

questions = [
    # ============ LISTENING Part 1 (Q1-5): pictures ============
    {"id": "l_p1", "type": "multiple_group", "section": "listening", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nYou will hear five short conversations. Choose the correct picture (A, B, or C).\nYou will hear each conversation twice.",
     "points": 5,
     "items": [
         {"q": "1. When does John offer to come?", "option_images": [IMG + "lq1_A.png", IMG + "lq1_B.png", IMG + "lq1_C.png"],
          "options": ["A", "B", "C"], "answer": 1},
         {"q": "2. What did the woman enjoy doing at the party?", "option_images": [IMG + "lq2_A.png", IMG + "lq2_B.png", IMG + "lq2_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "3. What will the weather be like in the morning?", "option_images": [IMG + "lq3_A.png", IMG + "lq3_B.png", IMG + "lq3_C.png"],
          "options": ["A", "B", "C"], "answer": 1},
         {"q": "4. What time does the tour of the hospital start?", "option_images": [IMG + "lq4_A.png", IMG + "lq4_B.png", IMG + "lq4_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "5. What isn't the daughter having for her birthday?", "option_images": [IMG + "lq5_A.png", IMG + "lq5_B.png", IMG + "lq5_C.png"],
          "options": ["A", "B", "C"], "answer": 0},
     ]},

    # ============ LISTENING Part 2 (Q6-10): gap-fill ============
    {"id": "l_p2", "type": "writing", "section": "listening", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nYou will hear a radio presenter called Jonathan talking about the programmes on during the week.\nFor each question, write the correct answer in the gap.",
     "title": "Radio Programmes",
     "passage": "There are (6) ________ to some of our programmes this week.\nThe wildlife documentary looks at (7) ________ and how to identify them.\nIn Writers' World, discover how to get your work (8) ________ by using the web.\nOn Sports Night, there will be no discussions on last week's matches as they were (9) ________.\nYou'll find Sally at the entrance to the (10) ________ on Friday.",
     "gap_items": ["CHANGES", "WILD FLOWERS", "PUBLISHED", "CANCELLED", "LIBRARY"],
     "gap_labels": ["6", "7", "8", "9", "10"],
     "points": 5},

    # ============ LISTENING Part 3 (Q11-15): MC ============
    {"id": "l_p3", "type": "multiple_group", "section": "listening", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nYou will hear an interview with a woman called Maggie Taylor, who is talking about garlic.\nChoose the correct answer A, B, or C.",
     "points": 5,
     "items": [
         {"q": "11. Maggie explains that", "options": ["she discovered garlic at university.", "you often find garlic in an English kitchen.", "people in the older generation don't like garlic."], "answer": 0},
         {"q": "12. Maggie says that because of learning about garlic", "options": ["she did a cookery course.", "she can now cook meals from other countries.", "she has travelled all over the world."], "answer": 1},
         {"q": "13. What does Maggie say about the health benefits of garlic?", "options": ["She thinks it can cure the common cold.", "It has been used as a medicine for many years.", "She has used it to help with a skin condition."], "answer": 1},
         {"q": "14. Maggie explains that", "options": ["garlic from the supermarket is OK to grow in an English garden.", "you can grow garlic in any climate.", "in the past it was harder to buy suitable garlic to grow in an English garden."], "answer": 2},
         {"q": "15. What does Maggie say about growing garlic?", "options": ["She wasn't successful the first time she tried.", "She has always had great results.", "You shouldn't dig it up while it's still green."], "answer": 0},
     ]},

    # ============ LISTENING Part 4 (Q16-20): YES/NO ============
    {"id": "l_p4", "type": "multiple_group", "section": "listening", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nYou will hear a woman called Martha and a man called James talking about a TV series called Madison, which is about a doctor who works in a hospital.\nDecide if each sentence is correct or incorrect. If it is correct, write YES. If it is not correct, write NO.",
     "points": 5,
     "items": [
         {"q": "16. They agree that the last show in the series was complicated.", "options": ["YES", "NO"], "answer": 0},
         {"q": "17. James believes that the series is successful because of the main character.", "options": ["YES", "NO"], "answer": 0},
         {"q": "18. They both admire the main character's behavior.", "options": ["YES", "NO"], "answer": 1},
         {"q": "19. Martha thinks that the main character has similar skills to a detective.", "options": ["YES", "NO"], "answer": 0},
         {"q": "20. They both plan to watch the series again.", "options": ["YES", "NO"], "answer": 1},
     ]},

    # ============ READING Part 1 (Q1-5): notices ============
    {"id": "r_p1", "type": "multiple_group", "section": "reading", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nLook at the text in each question. What does it say?\nCircle the correct letter A, B or C.",
     "points": 5,
     "items": [
         {"q": "1. What does it say?", "notice": "Hi Mary.\n\nI've cancelled my trip to Grandad's tomorrow as I'm not feeling very well.\nIf he calls can you tell him I'll phone him tonight?\n\nLove, Mum x",
          "options": ["Mary should call Grandad.", "Grandad has cancelled the visit.", "Mum will call Grandad later."], "answer": 2},
         {"q": "2. What does it say?", "notice": "Music School\nGuitar lessons 50% off from now until 31 August.\nClasses must be booked in advance.",
          "options": ["Lessons can be paid for on arrival.", "Guitar lessons are half price for a limited period.", "The school offers advanced music lessons."], "answer": 1},
         {"q": "3. What does it say?", "notice": "CAR PARK\nParking for customers only.\n1 hour maximum stay.\nManagement are not responsible for loss or damage to property.",
          "options": ["Parking is limited to one hour.", "Any damage should be reported to management.", "Any lost property should be handed in."], "answer": 0},
         {"q": "4. What does it say?", "notice": "To: sjenner@hotmail.com\nFrom: tom668@gmail.com\n\nI've booked your tickets for the flight. They were the cheapest I could get. You can check in online but can only take hand luggage or you have to pay extra.\n\nTom",
          "options": ["There are cheaper flights available.", "You have to pay extra for hand luggage.", "There's no need to check in at the airport."], "answer": 2},
         {"q": "5. What does it say?", "notice": "Sofa for sale\nAlmost new sofa needs a new home as we're moving to a small apartment.\nBuyer must collect.",
          "options": ["The sofa is perfect for a small apartment.", "The buyer must arrange to transport the sofa.", "The sofa is brand new."], "answer": 1},
     ]},

    # ============ READING Part 2 (Q6-10): matching people to jobs ============
    {"id": "r_p2", "type": "matching", "section": "reading", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nThe people below are all looking for a job.\nOn the opposite page there are descriptions of eight jobs.\nDecide which jobs would be the most suitable for the people below.",
     "events": [
         "A ABC Computer Specialists — Do you have customer service skills? ABC Computer Specialists are looking for sales advisers to join our growing customer service team. This is a full-time post, 37 hours a week, with great opportunities for the right person.",
         "B Mansion House Hotel — An exciting opportunity for students wanting work experience in the Mansion House Hotel on a part-time basis. You will be dealing with international customers and a second language would be an advantage. Hours of work can be agreed to suit your needs though you would be required to work some weekends.",
         "C Susie's Hairdressing — We are a new hairdresser's and we want a young, hard-working volunteer to manage our reception desk. You will take calls, make bookings and help build a relationship with our customers. Suitable candidates will be offered a one-year contract.",
         "D The Daily News — Our business is growing and we need an assistant for our customer service team. The successful person will assist in managing our sales staff and be responsible for reporting on sales. The successful person will receive training.",
         "E Amega — Would you like to work in a modern office environment, building relationships with customers, and working with our excellent team? If you've recently completed your studies at university and are looking for a career in the beauty industry, then please get in contact.",
         "F Peterfield Forum — We are looking for keen volunteers to help run our summer school. You will have experience in working with young people and be prepared to accompany them on trips. The school is open from Monday to Friday and we need volunteers for at least two of these days.",
         "G Hall Green Community Centre — This is a great opportunity to gain experience in youth work. We are looking for a volunteer with work experience to support our young people as they begin to enter employment. You would be expected to work on Saturdays from 9 a.m. to 5 p.m. with occasional Sunday sessions.",
         "H Lucas Media — Are you a student looking for work from Monday to Friday over the vacation period? We are offering a short-term contract to a keen young person to work with our sales team. You will get an idea of how a modern company operates, deal with customer enquiries and have the chance to help develop our website.",
     ],
     "options": [
         "6. Sandra is doing a four-year degree in hair and beauty and wants to work as a volunteer for her third-year work experience. She likes to be part of a team and would enjoy dealing with customers.",
         "7. Manuela is from Spain and is looking for work to support herself financially while she studies English at a local college. She can only work on Saturdays and Sundays and some evenings.",
         "8. Stella is looking for work during the holidays. She's studying business at college and would love somewhere she can gain experience in a business environment and put her IT skills into practice.",
         "9. John is looking for a job where he can work with customers. He recently completed a course in this area of work and is keen to find a job that would offer support in developing skills in managing staff.",
         "10. Simon has a job but wants to work with teenagers during the weekend. He is planning a career change and is happy to work without pay in order to gain experience.",
     ],
     "items": ["A ABC Computer Specialists", "B Mansion House Hotel", "C Susie's Hairdressing",
               "D The Daily News", "E Amega", "F Peterfield Forum",
               "G Hall Green Community Centre", "H Lucas Media"],
     "answer": [2, 1, 7, 3, 6],  # Q6=C Q7=B Q8=H Q9=D Q10=G
     "points": 5},

    # ============ READING Part 3 (Q11-15): YES/NO ============
    {"id": "r_p3", "type": "multiple_group", "section": "reading", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nLook at the sentences below about trips to the Great Bear Rainforest.\nRead the text to decide if each sentence is correct or incorrect. If it is correct, write YES. If it is not correct, write NO.",
     "title": "Explore The Great Bear Rainforest",
     "passage": "The Great Bear Rainforest is on an island on British Columbia's central coast, in Canada. The rainforest is the largest remaining piece of unbroken rainforest in the world and is full of interesting plants, birds and animals, including the Spirit Bear. It is thought that there are no more than 400 of these bears in the whole of the Great Bear Rainforest — and they don't exist anywhere else in the world.\n\nThe island is a fantastic place to go bear and whale watching. It is also a great place to go diving, snorkelling and fishing. Even better, tourism is encouraged by local people and conservationists, as it shows that money can be made from the island without changing it, and this helps to protect the rainforest.\n\nOne of the best times to visit the island is mid-September. This is when salmon return in great numbers from the Pacific Ocean to the streams and rivers of British Columbia's west coast. It is also when the bears come out to hunt them!\n\nKnight Inlet is a place well known for its population of grizzly bears. It is on the southern edge of the Great Bear Rainforest. There can be up to 40 bears within a few miles during autumn when the fish are swimming up the river. Guests who stay at Knight Inlet start their adventure with a boat ride. They then board a small bus and travel through the northern rainforest to the river. They can go to five different viewing platforms, in three different areas, which are specially built to provide a safe and comfortable place to watch the bears from. It is not uncommon to see 10-15 bears on the river at a time.\n\nAutumn isn't the only season that grizzly bears go to the area. Starting in April, when they've woken from their winter sleep, both black and grizzly bears arrive to feed on the new spring growth. Even in mid-summer, when many of the bears have moved into the forests for their food, you can see several bears each day.",
     "points": 5,
     "items": [
         {"q": "11. The Great Bear Rainforest is divided into several parts.", "options": ["YES", "NO"], "answer": 1},
         {"q": "12. People who live in the area welcome tourists.", "options": ["YES", "NO"], "answer": 0},
         {"q": "13. Knight Inlet is in the middle of the rainforest.", "options": ["YES", "NO"], "answer": 1},
         {"q": "14. There is a choice of places to see the bears from.", "options": ["YES", "NO"], "answer": 0},
         {"q": "15. All tourists must sleep more than one night at Campbell River.", "options": ["YES", "NO"], "answer": 1},
     ]},

    # ============ READING Part 4 (Q16-20): MC ============
    {"id": "r_p4", "type": "multiple_group", "section": "reading", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nFor each question, choose the correct answer.",
     "title": "Headteacher Mary Collins talks about healthy school days",
     "passage": "Since I took up my role of Head at Franley Junior School I have been keen to educate our children on the importance of developing healthy habits. I started by working with our restaurant manager to come up with tasty new menus that contain lots of healthy ingredients. We change the menu Monday to Friday to encourage the children to try different things and keep unhealthy fried food to a minimum. The children have enjoyed the meals and eat a wide range of fruit and vegetables.\n\nWe've also rented an area of land near the school for a vegetable garden and made gardening a part of the school curriculum. Children now prepare the ground for planting, plant the seeds and watch as these turn into healthy fruit and vegetable plants. We're planning to create a child-friendly kitchen so our pupils can discover the pleasure of cooking. I believe all this gives the children an understanding of where our food comes from and very important skills that will stay with them for life.\n\nTo support this healthy-eating campaign, we have also made changes to the amount of physical exercise we get our children to do during the day. We start every morning before classes with a 'wake and shake' session in the playground when children get the chance to burn off energy with fun exercise routines. We also have different play times during the day so the playground isn't crowded, which means the children can run around safely. To support this we have also invested in sports equipment such as tennis, football and gym equipment to encourage the youngsters to take up sports.\n\nBut it's not just the children who are developing a healthy lifestyle. Several of our teachers have signed up for the Franley Fun Run this summer for the first time and have started a training programme in order to get fit. Many of our pupils have joined them and will be taking part in the run as well. I'm sure that seeing their teachers beside them will inspire them to finish. We have even had several parents show an interest in doing the event as well, so this is something we're all really looking forward to.",
     "points": 5,
     "items": [
         {"q": "16. Since Mary joined the school", "options": ["fried food is no longer on the menu.", "the school has employed a new restaurant manager.", "the menu changes daily."], "answer": 2},
         {"q": "17. What does Mary say about gardening?", "options": ["It is part of a course of study.", "The children are producing food for the school kitchen.", "The children are learning to cook the food they grow."], "answer": 0},
         {"q": "18. Play times", "options": ["only take place at the start of the day.", "result in the playground getting crowded.", "are timed to prevent accidents."], "answer": 2},
         {"q": "19. What does Mary say about the teachers?", "options": ["They are all doing the fun run.", "They are training with the children.", "They have done the fun run before."], "answer": 1},
         {"q": "20. What would be a good introduction to this article?", "options": ["Franley's new Head Mary Collins explains how she set about getting fit with the children.", "Read how Mary Collins, the new school Head, reacted when she was ordered to improve the quality of food on the school menu.", "Mary Collins explains how the first aim she set herself in her new job was to create a focus on healthy living."], "answer": 2},
     ]},

    # ============ READING Part 5 (Q21-25): gap-fill MC ============
    {"id": "r_p5", "type": "multiple_group", "section": "reading", "part": 5, "start_num": 21,
     "instruction": "Part 5. Questions 21-25.\nFor each question, choose the correct answer.",
     "title": "Light Pollution",
     "inline_gaps": True,
     "passage": "We are all familiar with air pollution, (21) ________ if we live in busy cities and suffer with pollution from factories and heavy traffic. But many of us don't take light pollution (22) ________. Compared to the skies of our grandparents, the night isn't (23) ________ as dark as it used to be because the use of artificial lighting has increased. As a result, this can create problems for migrating birds, which are not able to use the moon and stars to (24) ________ their journey. In addition, light from our neighbourhood, whether that is street lighting, (25) ________ lights or passing cars, can also influence our own sleep patterns. And of course, the night sky is harder for us to see unless we go to parts of the world free of artificial lighting.",
     "points": 5,
     "items": [
         {"q": "21. air pollution, (21) ________ if we live in busy cities", "options": ["really", "especially", "because", "when"], "answer": 1},
         {"q": "22. don't take light pollution (22) ________.", "options": ["seriously", "real", "mainly", "important"], "answer": 0},
         {"q": "23. the night isn't (23) ________ as dark", "options": ["just", "quite", "equal", "same"], "answer": 1},
         {"q": "24. use the moon and stars to (24) ________ their journey.", "options": ["fly", "leave", "set", "complete"], "answer": 3},
         {"q": "25. whether that is street lighting, (25) ________ lights or passing cars", "options": ["danger", "security", "guard", "guarantee"], "answer": 1},
     ]},

    # ============ WRITING ============
    {"id": "w1", "type": "writing", "section": "writing", "start_num": 1,
     "question": "This is part of an email you receive from an English friend, Tony:\n\nFrom: Tony\nSubject: I need your advice\n\nI'm not sure how to spend my summer holiday. My teacher suggests volunteering at the local hospital, which could be a good experience for the future. But honestly, I also feel very tired after exams and just want to relax at home and watch films. What do you think would be the best choice for me?\n\nNow write an email, giving your friend your opinion and some suggestions.\n\nWrite at least 100 words.",
     "word_limit": "100", "points": 20},
]

test = {
    "section": "b1plus_end",
    "title": "B1+ · END",
    "icon": "📕",
    "time_limit": 55,
    "price": 0,
    "original_price": 0,
    "active": True,
    "description": "B1+ daraja yakuniy imtihoni — Listening + Reading + Writing",
    "audio_parts": [AUDIO, AUDIO, AUDIO, AUDIO],
    "created_at": datetime.now(timezone.utc),
    "questions": questions,
}

def seed_b1plus_end(db):
    """Insert or update the B1+ END test document (keeps _id stable)."""
    db.tests.update_one({"section": "b1plus_end"}, {"$set": test}, upsert=True)
    return len(test["questions"])
