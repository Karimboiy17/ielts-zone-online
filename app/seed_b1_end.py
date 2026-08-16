"""Auto-seed B1 END test data into MongoDB (used at app startup on Railway)."""
from datetime import datetime, timezone

AUDIO = "/static/audio/b1_end_listening_full.mp3"
IMG = "/static/images/b1_end/"

questions = [
    # ============ LISTENING Part 1 (Q1-5): pictures ============
    {"id": "l_p1", "type": "multiple_group", "section": "listening", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nYou will hear five short recordings. For each question, choose the correct picture.\nYou will hear each recording twice.",
     "points": 5,
     "items": [
         {"q": "1. What did the man refuse to do?",
          "option_images": [IMG + "lq1_A.png", IMG + "lq1_B.png", IMG + "lq1_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "2. What was the woman doing when her phone rang?",
          "option_images": [IMG + "lq2_A.png", IMG + "lq2_B.png", IMG + "lq2_C.png"],
          "options": ["A", "B", "C"], "answer": 0},
         {"q": "3. What has the man stopped doing recently?",
          "option_images": [IMG + "lq3_A.png", IMG + "lq3_B.png", IMG + "lq3_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "4. How did the man travel around when he was on holiday?",
          "option_images": [IMG + "lq4_A.png", IMG + "lq4_B.png", IMG + "lq4_C.png"],
          "options": ["A", "B", "C"], "answer": 0},
         {"q": "5. Which person does the woman feel closest to?",
          "option_images": [IMG + "lq5_A.png", IMG + "lq5_B.png", IMG + "lq5_C.png"],
          "options": ["A", "B", "C"], "answer": 2},
     ]},

    # ============ LISTENING Part 2 (Q6-10): gap-fill ============
    {"id": "l_p2", "type": "writing", "section": "listening", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nYou will hear a woman on the radio talking about a charity event in her area.\nFor each question, write the correct answer in the gap.",
     "title": "Cakes for Charity",
     "passage": "Name of charity: Rose Children's Hospital\nDate of cake sale: (6) ________\nHelpers needed to make and sell cakes and arrange tables.\nPlace for cake sale if wet outside: (7) ________\nTime: 9.30 – (8) ________\nMoney organisers hope to make: (9) ________\nMoney will be used for: (10) ________",
     "gap_items": ["July 17", "Indoor market", "3:15", "£450", "The garden play area"],
     "gap_labels": ["6", "7", "8", "9", "10"],
     "points": 5},

    # ============ LISTENING Part 3 (Q11-15): MC ============
    {"id": "l_p3", "type": "multiple_group", "section": "listening", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nYou will hear a woman called Karen talking about a journey she made.\nFor each question, choose the correct answer.",
     "points": 5,
     "items": [
         {"q": "11. Why did Karen go to Jakarta?",
          "options": ["to do a job", "to visit friends", "for a holiday"],
          "answer": 0},
         {"q": "12. How did Karen learn about Indonesia before she went there?",
          "options": ["from the internet", "from a book", "from a friend's letter"],
          "answer": 0},
         {"q": "13. What did Karen dislike about Jakarta?",
          "options": ["the weather", "the traffic", "the buildings"],
          "answer": 1},
         {"q": "14. What reminds Karen of Jakarta?",
          "options": ["her photographs", "her sandals", "a sculpture"],
          "answer": 1},
         {"q": "15. When Karen returns to Indonesia, she's hoping to",
          "options": ["visit a number of islands.", "see more of Jakarta.", "experience the rainy season."],
          "answer": 0},
     ]},

    # ============ LISTENING Part 4 (Q16-20): YES/NO ============
    {"id": "l_p4", "type": "multiple_group", "section": "listening", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nYou will hear a conversation between a girl, Alice, and a boy, Mark, about celebrities.\nDecide if each sentence is correct or incorrect.\nIf it is correct, choose YES. If it is incorrect choose NO.",
     "points": 5,
     "items": [
         {"q": "16. Mark and Alice both think famous people have a lot of advantages.",
          "options": ["YES", "NO"], "answer": 1},
         {"q": "17. Alice and Mark agree about why celebrities wear dark glasses.",
          "options": ["YES", "NO"], "answer": 1},
         {"q": "18. Mark turns down Alice's offer of a book.",
          "options": ["YES", "NO"], "answer": 0},
         {"q": "19. Mark believes Alice would enjoy being a famous person.",
          "options": ["YES", "NO"], "answer": 0},
         {"q": "20. Mark changes his opinion about being famous at the end.",
          "options": ["YES", "NO"], "answer": 1},
     ]},

    # ============ READING Part 1 (Q1-5): notices ============
    {"id": "r_p1", "type": "multiple_group", "section": "reading", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-5.\nLook at the text in each question. What does it say?\nFor each question, circle the correct letter A, B, or C.",
     "points": 5,
     "items": [
         {"q": "1. What does it say?", "notice": "Royal Theatre\nWe ask you to turn off all electronic devices.",
          "options": ["no devices are allowed in the theatre.", "do not leave your phone switched on.", "the volume on your phone should be low."],
          "answer": 1},
         {"q": "2. What does it say?", "notice": "GLB Trains\nYour opinions are important —\nComment Forms are available online and at the ticket office.",
          "options": ["The company wants to know what you think of its services.", "If you have a complaint, you can tell staff at the ticket office.", "Go to the manager's office to hand in your Comment Forms."],
          "answer": 0},
         {"q": "3. What does it say?", "notice": "Attention Drivers!\nWe're replacing all the street lights.\nWe regret there may be long delays.",
          "options": ["An earlier accident has caused a long traffic jam.", "Traffic is queuing because there are workers here.", "This part of the road is closed because there are no lights."],
          "answer": 1},
         {"q": "4. What does it say?", "notice": "NOTICES\nNEW INTERNATIONAL HOTEL TO OPEN HERE NEXT JANUARY\nWE WILL NEED RECEPTIONISTS, WAITERS, KITCHEN STAFF\nPEOPLE WITH THE SUITABLE SKILLS ARE INVITED TO APPLY NOW",
          "options": ["The hotel needs people to start work now.", "If you are looking for a job, you might find one here.", "When the hotel opens, you can apply for work."],
          "answer": 1},
         {"q": "5. What does it say?", "notice": "Want to get a loan but get confused about which one would be best for you?\nGo to www.BestDeal4Me.com\nWe compare all the main banks.",
          "options": ["Visit this website for information about the various loans you can apply for.", "You'll be able to borrow some money from this company if you contact them.", "BestDeal4Me loans are similar to those offered by other banks."],
          "answer": 0},
     ]},

    # ============ READING Part 2 (Q6-10): matching people to TV programmes ============
    {"id": "r_p2", "type": "matching", "section": "reading", "part": 2, "start_num": 6,
     "instruction": "Part 2. Questions 6-10.\nThe people below all want to watch something on TV. On the opposite page there are descriptions of eight TV programmes.\nDecide which programme would be the most suitable for the people below.",
     "points": 5,
     "events": [
         "Show Me How — In today's programme Gemma and her best friend Louise will show you how to make a delicious banana bread. Mums or dads should remember to get the ingredients ready so you can follow the friends' instructions during the show.",
         "The Big Chase — When the police start their investigation into a series of robberies, they expect to be making an early arrest. However, they are not prepared for the danger around every corner. A very exciting story that is sure to keep you on the edge of your seat. This week's late-night film starts at 12.30.",
         "Brain of Britain — On this week's quiz show for the very clever we have a taxi driver, a lawyer, a journalist and a gardener answering questions. The winner will go through to the final next month with the chance of being crowned Brain of Britain. See how many questions you can answer!",
         "Front Row — Join our team of experts as they discuss the draw for the next round of the FA Cup. Find out who will be playing who when they meet for the next round in two weeks' time. We'll have reporters out and about interviewing players on their opinions of the draw.",
         "5-2-1 — Join your host Sam Daniels as a team of friends from university try to answer questions on general knowledge and their favourite subjects. Can they win the top prize of £20,000? Join us just after the lunchtime news at 1.30.",
         "Molly and Me — In this week's programme Molly reads another story from a well-known children's author. For five- to eight-year-olds – sit together with your child and enjoy some quiet time as you follow the story with Molly and her friends.",
         "Last Summer — When Greg and Sandra meet on a coach journey to Athens, they quickly realise they have so much in common. They decide to spend the following two weeks together, fall in love and dream of a future together. However, life gets in the way. A short but very enjoyable 90-minute film.",
         "Midweek — In tonight's game you can see two teams both playing at their very best. The programme begins at 7.00 and the game starts at 7.30. Stay around after the match for views from our team of professional players and managers as they discuss the result and choose their man of the match.",
     ],
     "options": [
         "6. Lorraine is having a day off work with a cold. She wants to watch a quiz show during the afternoon especially one with cash prizes.",
         "7. Gary can't sleep and wants to see if there is anything on TV. He'd like to watch a film and enjoys crime thrillers or anything with lots of action.",
         "8. Isabelle is babysitting a seven-year-old girl. She's looking for a children's programme that has anything to do with drawing or cooking so they can do it together.",
         "9. Raj and his wife Grace are spending the evening at home and are keen to watch a film together. They would like to watch something romantic and not anything that's too long.",
         "10. Robert has some friends coming round for the evening. He would like a programme showing live football that has experts discussing the game afterwards.",
     ],
     "items": ["A Show Me How", "B The Big Chase", "C Brain of Britain", "D Front Row",
               "E 5-2-1", "F Molly and Me", "G Last Summer", "H Midweek"],
     "answer": [4, 1, 0, 6, 7]},

    # ============ READING Part 3 (Q11-15): YES/NO The truth about telling lies ============
    {"id": "r_p3", "type": "multiple_group", "section": "reading", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-15.\nLook at the sentences below about some research into telling lies.\nRead the text to decide if each sentence is correct or incorrect.\nIf it is correct, choose Yes. If it is not correct, choose No.",
     "title": "The truth about telling lies",
     "passage": "Leonard Saxe, Ph.D., a psychology expert at Brandeis University, thinks that telling lies has been a part of everyday life for a long time. Yet it is only recently that it has become a topic for discussion among psychologists. Before that, lies were mainly things that religious leaders were concerned about.\n\nAs psychologists look more closely at how honest we are, they are discovering that it is surprisingly common to tell lies. In 1996, Bella DePaulo, PhD., a psychologist at the University of Virginia, studied 147 people between the ages of 18 and 71 who had to keep a diary of all the lies they told over a period of a week. The results showed that most people told lies once or twice a day and that some types of relationships involve more lies than others. More untruths were told between teenagers and parents than between complete strangers.\n\nThough some lies can cause problems between people, others may actually make it easier for people to get on well. In DePaulo's group, one in every four of the lies were told to make another person feel better. In fact, lies in which people say they like someone or something more than they actually do (\"Your cakes are the best\") are about 10 to 20 times more common than lies in which people say they like someone less than they really do. When the researchers counted the lies, they didn't include the everyday, polite lies we say to each other, such as \"I'm fine, thanks,\" when actually we don't feel well, or \"No trouble at all,\" when really we are a bit annoyed.",
     "points": 5,
     "items": [
         {"q": "11. Lies have been studied in psychology for many years.",
          "options": ["Yes", "No"], "answer": 1},
         {"q": "12. DePaulo asked a group of people to note down their lies for a whole week.",
          "options": ["Yes", "No"], "answer": 0},
         {"q": "13. DePaulo discovered that lies were more likely between people who had only just met.",
          "options": ["Yes", "No"], "answer": 1},
         {"q": "14. DePaulo realised that the purpose of most lies was to be kind.",
          "options": ["Yes", "No"], "answer": 0},
         {"q": "15. The researchers in DePaulo's study counted all kinds of lies.",
          "options": ["Yes", "No"], "answer": 1},
     ]},

    # ============ READING Part 4 (Q16-20): MC How to study ============
    {"id": "r_p4", "type": "multiple_group", "section": "reading", "part": 4, "start_num": 16,
     "instruction": "Part 4. Questions 16-20.\nRead the text and questions below.\nFor each question, circle the correct answer A, B, or C.",
     "title": "How to study – online or in the classroom?",
     "passage": "Some people prefer the traditional way of learning – in a classroom, with a teacher and other students. However, more people are turning to studying online. Gonzalo Lopez, who wanted to study business in English, was one of these. His first course was in a classroom, but he realised it might take longer to progress than he thought at first. He couldn't afford to stay at college and so, having good IT skills, he began an online course. Gonzalo says his online teacher was good, but he doesn't think studying on your own is as enjoyable as being with your friends in class.\n\nMuneera Farzath has another opinion. Sometimes she got to lessons early or stayed on after they finished, because she said it was difficult for her to study with so much happening in the classroom. She didn't dislike the people in class with her, but says that studying online is more peaceful. Muneera also thinks there are advantages to studying alone with a teacher who has got time just for you. She says she's a slow learner and the teacher has made some suggestions about maybe buying apps that would help her.\n\nAfter three months studying online, Gonzalo Lopez returned to study at college. Although he had thought the online and college courses were similar, Gonzalo, who is Spanish, found it difficult to study online in English. In the classroom, with English students, it was easier.\n\nMy personal experience is of studying Arabic in a classroom and online. And I can see the advantages and disadvantages of each type of course. If it's possible for you, I'd recommend doing a bit of both. If you do this, you'll have the best chance of success.",
     "points": 5,
     "items": [
         {"q": "16. Why did Gonzalo change to an online course?",
          "options": ["to learn technology skills", "to have longer lessons", "to save money"],
          "answer": 2},
         {"q": "17. What do we learn about Muneera's time in the classroom?",
          "options": ["She got annoyed with some students.", "She found it hard to concentrate.", "She had to leave the lessons early."],
          "answer": 1},
         {"q": "18. What does Muneera now have which she didn't have before?",
          "options": ["a personal one-to-one teacher", "some free apps for studying", "a chance to study more quickly"],
          "answer": 0},
         {"q": "19. What problem did Gonzalo have with online studying?",
          "options": ["the subject", "the course", "the language"],
          "answer": 2},
         {"q": "20. Which statement explains the writer's opinion?",
          "options": ["Work hard and you'll succeed using either way.", "A combination of the two ways of studying is best.", "Most people will turn to learning online in future."],
          "answer": 1},
     ]},

    # ============ READING Part 5 (Q21-25): gap-fill MC ============
    {"id": "r_p5", "type": "multiple_group", "section": "reading", "part": 5, "start_num": 21,
     "instruction": "Part 5. Questions 21-25.\nRead the text below and choose the correct answer for each gap.",
     "inline_gaps": True,
     "passage": "Insect bites are common and generally cause the skin to feel slightly uncomfortable. In the UK, there are a number of animals (21) ________ may bite humans, including mosquitoes and spiders.\n\nUsually, bites are not dangerous but sometimes a person may (22) ________ allergic to the bite. People like this (23) ________ see a doctor immediately as it is important to get treatment quickly. If it is difficult to breathe or the symptoms are (24) ________, then don't delay. Go to a hospital straight away.\n\nOn most occasions, however, bites can be dealt with very easily at home. Wash the affected area of skin and try to (25) ________ touching it, even though it feels itchy.",
     "points": 5,
     "items": [
         {"q": "21. In the UK, there are a number of animals (21) ________ may bite humans.",
          "options": ["who", "that", "what"], "answer": 1},
         {"q": "22. but sometimes a person may (22) ________ allergic to the bite.",
          "options": ["find", "be", "have"], "answer": 1},
         {"q": "23. People like this (23) ________ see a doctor immediately.",
          "options": ["might", "need", "must"], "answer": 2},
         {"q": "24. If it is difficult to breathe or the symptoms are (24) ________, then don't delay.",
          "options": ["serious", "ugly", "anxious"], "answer": 0},
         {"q": "25. Wash the affected area of skin and try to (25) ________ touching it.",
          "options": ["avoid", "miss", "refuse"], "answer": 0},
     ]},

    # ============ WRITING ============
    {"id": "w1", "type": "writing", "section": "writing", "start_num": 1,
     "question": "This is part of an email you receive from an English friend, Travis:\n\nFrom: Travis\nI need your advice\nI often eat fast food because I'm too busy to cook. But I know it isn't healthy, and I don't feel good. Do you think I should change my habits? How can I eat better without spending too much time or money?\n\nNow write an email, giving your friend some advice.\nWrite at least 100 words.",
     "word_limit": "100", "points": 20},
]

test = {
    "section": "b1_end",
    "title": "📗 B1 · END",
    "icon": "📗",
    "time_limit": 55,
    "price": 0,
    "original_price": 0,
    "active": True,
    "description": "B1 daraja yakuniy imtihoni — Listening + Reading + Writing",
    "audio_parts": [AUDIO, AUDIO, AUDIO, AUDIO],
    "created_at": datetime.now(timezone.utc),
    "questions": questions,
}

def seed_b1_end(db):
    """Insert or update the B1 END test document (keeps _id stable so old attempts work)."""
    db.tests.update_one(
        {"section": "b1_end"},
        {"$set": test},
        upsert=True,
    )
    return len(test["questions"])
