"""Auto-seed B1+ MID test data into MongoDB (used at app startup on Railway)."""
from datetime import datetime, timezone

# ============ AUDIO PARTS (B1+ MID Listening) ============
A1 = "/static/audio/b1mid_listening_full.mp3"
A2 = "/static/audio/b1mid_listening_full.mp3"
A3 = "/static/audio/b1mid_listening_full.mp3"
A4 = "/static/audio/b1mid_listening_full.mp3"
audio_parts = [A1, A2, A3, A4]

IMG = "/static/images/b1mid/"

LISTENING_QUESTIONS = [
    {"id": "l_p1", "type": "multiple_group", "section": "listening", "part": 1, "start_num": 1,
     "question": "You will hear five short conversations. Choose the correct picture (A, B, or C).\nYou will hear each conversation twice.",
     "points": 5,
     "items": [
         {"q": "1. What does mum say Helen's brother can eat?", "image": IMG + "lq1.png",
          "options": ["A", "B", "C"], "answer": 1},
         {"q": "2. What does the man complain about?", "image": IMG + "lq2.png",
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "3. At what time might the road be OK to use?", "image": IMG + "lq3.png",
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "4. How much is a return flight to Paris at the moment?", "image": IMG + "lq41.png",
          "options": ["A", "B", "C"], "answer": 0},
         {"q": "5. Which programme has been cancelled?", "image": IMG + "lq42.png",
          "options": ["A", "B", "C"], "answer": 1},
     ]},
    {"id": "l_p2", "type": "writing", "section": "listening", "part": 2, "start_num": 6,
     "question": "You will hear a manager called Sandra talking about a company training day.\nFor each question, write the correct answer in the gap.",
     "title": "Company Training Day",
     "passage": "Some of the training sessions may take place in a (6) ________ to the one in the programme.\nYour training sessions will be confirmed by email on (7) ________.\nPlease complete the (8) ________ in the materials before you come to the training event.\nPlease give your completed questionnaire to the (9) ________ after the training day.\nThe (10) ________ will be closed on the training day.",
     "gap_items": ["DIFFERENT BUILDING", "13 SEPTEMBER", "EXERCISES", "TRAINING MANAGER", "(COMPANY) RESTAURANT"],
     "gap_labels": ["6", "7", "8", "9", "10"],
     "points": 5},
    {"id": "l_p3", "type": "multiple_group", "section": "listening", "part": 3, "start_num": 11,
     "question": "You will hear an interview with a student called Emily, who walks people's dogs.\nChoose the correct answer A, B, or C.",
     "points": 5,
     "items": [
         {"q": "11. What does Emily say about walking dogs?",
          "options": ["It's a good business idea.", "It pays for some of her living expenses.", "It helps people get out of their house."],
          "answer": 1},
         {"q": "12. Emily says her first customer",
          "options": ["was her neighbour.", "was in hospital at the time.", "made her accept some money."],
          "answer": 2},
         {"q": "13. What does Emily say about becoming a dog walker?",
          "options": ["She enjoyed what she was doing.", "She had trouble arranging the walks around her studies.", "She spoke to people in the local shops."],
          "answer": 0},
         {"q": "14. Emily explains that",
          "options": ["she didn't get any work straightaway.", "she went to a customer's house.", "she met her first customer at the weekend."],
          "answer": 0},
         {"q": "15. Emily says that her customers",
          "options": ["are very busy.", "expect her to help them whenever they need it.", "have well-behaved dogs."],
          "answer": 2},
     ]},
    {"id": "l_p4", "type": "multiple_group", "section": "listening", "part": 4, "start_num": 16,
     "question": "You will hear a woman called Anne and a man called Peter talking about a college party.\nDecide if each sentence is correct or incorrect.\nIf it is correct, write YES. If it is not correct, write NO.",
     "points": 5,
     "items": [
         {"q": "16. Peter wants to take his sister to the party.",
          "options": ["YES", "NO"], "answer": 1},
         {"q": "17. Anne hopes the party will be bigger than the one last year.",
          "options": ["YES", "NO"], "answer": 1},
         {"q": "18. Peter thinks the new college hall is big enough for the party.",
          "options": ["YES", "NO"], "answer": 0},
         {"q": "19. Peter thinks DJs play a good range of music.",
          "options": ["YES", "NO"], "answer": 1},
         {"q": "20. Peter is confident the party will end after midnight.",
          "options": ["YES", "NO"], "answer": 0},
     ]},
]

EVENTS = [
    "Open Air Entertainment — From old black-and-white classics to the latest award-winning films. We open for the summer season this Saturday. Come along and enjoy your favourite film in the evening, outside under the stars! Children under 13 enter for free.",
    "Find Robert the Rabbit — Bring the children along to our annual 'Find Robert' event at Kings Shelley Park this Saturday morning. Each year Robert finds a different place to hide away. Lots of running around and fun for children of all ages!",
    "Open Gardens — We're pleased to announce this popular summer event will be taking place this weekend. For anyone interested in gardens and gardening, now's your chance to have a look at some of the best in town as people open up their gardens to visitors any time between 9.00 and 5.00. Children are welcome.",
    "Tom and Larry's Garden Party — This Sunday Tom and Larry will be performing your favourite tunes and a few new ones you may not have heard of. Entrance fee for the evening entertainment includes an evening of music, a buffet with a wide range of food and hot and cold drinks along with ice-cream for the kids.",
    "Mansfield Arts Market — Come along this Sunday to check out some of the fantastic artistic talent the region has to offer. Have a look at some of the works and support our local artists by buying one to take home. We also have facepainting for the younger children and an art workshop for children who want to have a go themselves.",
    "Art Attack — Come along to our art club for children this weekend. We offer a safe place where children from 6-16 can have time working alone or with others on a piece of art. And if your child needs help with their schoolwork there'll be someone available to offer help and advice.",
    "Wanted: Young Musicians — For ages 14 and over, Middlechurch Musicians are holding a series of activities over the weekend for young people of any ability to learn or practise an instrument of their choice. Bring your child and their favourite instrument along, or if they haven't got to this stage let them try one of our own.",
    "Hassocks Green Festival — In addition to our regular favourites, organisers this year have introduced a children's theme. Take a chair, then relax and enjoy action films and some of the funniest cartoons that will keep your kids entertained. The festival opens on Sunday at 10.00 and is free.",
]

MOTORBIKE_TEXT = """I began riding motorbikes when I was eighteen years old, as a passenger on the back of my friend Luke's bike. It was a classic motorbike – big, fast, and noisy! Our first few rides were short trips – which he was very careful to make as enjoyable as possible for me – and as a result I fell in love with the whole motorbike experience almost immediately.

After a couple of months of shorter rides, we went on a longer group ride with Luke's motorcycling club, which he said would give me a good idea of the pleasures and difficulties of motorcycling. We rode approximately 100 km in one day, and it was a great experience – although we only managed to get less than half of the way to our destination. The ride was wonderful and we had beautiful weather as we went along the quiet roads. However, after we'd stopped to have a rest and were about to carry on riding, one rider in the group, Tania, suddenly found her bike wouldn't start. Some people in the group finally managed to get it going, but in the end Tania had to turn round and go back home by herself, knowing that if she stopped anywhere, she wouldn't be able to start her bike again. She bravely decided she could ride back home alone, but I doubted whether I'd have such a confident attitude in the same situation.

Our group then drove on to the mountains and stopped for some lunch – and that's where things started to go wrong. The weather turned bad and it began to snow. Then, without asking anyone, the leader of the group had the idea of going in a completely new direction up a steep mountain road, with corners that would be difficult for motorbikes even when the weather was good – and by now it was snowing quite heavily!

When we finally made it to the top of the mountain, Luke was annoyed. He said it was too risky to be on a mountain in such bad weather, and that we should go back down. We were both frozen when we reached the bottom, despite our cold-weather clothes. However, when we got back to my house we both began to see the funnier side of it all, and I immediately asked Luke when we could go again. I realised I could handle the worst of times on a motorbike, and there and then I made up my mind to try and save up for one."""

ROBERT_TEXT = """Like all children, I was always getting myself and the kitchen table in a mess when I first took an interest in painting. Unlike many kids, who give up activities like art for other subjects when they go through school, I continued painting throughout my childhood. Now, after years of enjoyment, I've finally taken the scary decision to show off some of my favourite pieces of work by holding an exhibition at Glebe Street library. Inviting people to see my work is a new idea and one which I'm looking forward to.

I've never had any formal art training. When I was trying to decide what I should study at university, art as a subject never entered my head. I always thought my parents wanted me to follow a subject that would be useful when I was looking for a job, so I ended up taking a business course. Looking back, my parents would probably have supported me whatever my decision, but I decided to do what I thought was best for everyone.

And during my time at university, I rarely did much in the way of painting. It wouldn't have been easy to paint anyway as I lived in university accommodation and had very little space. I kept an interest in art though and visited local exhibitions whenever I could, but that was about it. It was later in my thirties while I was working that I discovered my love of the activity again. Since then I've made a point of spending at least one evening a week painting.

However, my works have only ever been seen by trusted friends and relatives. They've always given me plenty of support and encouraged me to continue with my art. But I've always wondered what people who I didn't know would think, people who could give me an honest opinion of my ability. The library have been very helpful and offered me a room for the show. They've asked me to supply questionnaires about the event and I've included a section for visitors' comments about the works. I'm very much looking forward to reading these opinions."""

MAMBA_TEXT = """A bite from the Black Mamba is (21) ________ the 'kiss of death' in South Africa and it is (22) ________ a very dangerous snake. The venom can kill a person within 30 minutes to a few hours (23) ________ medical help. It is one of the world's fastest snakes as well and can travel at up to 16 kilometres an hour, though it uses this speed to (24) ________ danger rather than to attack. In fact, the Black Mamba is a rather (25) ________ creature and will avoid people if possible. It can measure anywhere between two and four metres long and, depending on the area where it lives, can be a different colour, from brown to green to grey. It gets its name from the inside of its mouth, which is ink black."""

READING_QUESTIONS = [
    {"id": "r_p1", "type": "multiple_group", "section": "reading", "part": 1, "start_num": 1,
     "question": "Look at the text in each question.\nWhat does it say?\nCircle the correct letter A, B or C.",
     "instruction": "Look at the text in each question.\nWhat does it say?\nCircle the correct letter A, B or C.",
     "points": 5,
     "items": [
         {"q": "1. What does it say?", "image": IMG + "rq1_q.png",
          "options": ["Get £10 off all sales.", "Offer lasts two weeks.", "Spend up to £50 and save £10."],
          "answer": 1},
         {"q": "2. What does it say?", "image": IMG + "rq2_q.png",
          "options": ["Charles can't meet Paul at 9.00.", "Charles will email Paul.", "Paul should confirm that 9.00 is OK."],
          "answer": 2},
         {"q": "3. What does it say?", "image": IMG + "rq3_q.png",
          "options": ["The waiter will explain our special meals of the day.", "Inform us of any issues with your diet.", "Orders must be paid for before you eat."],
          "answer": 1},
         {"q": "4. What does it say?", "image": IMG + "rq41_q.png",
          "options": ["Tracy needs to take a taxi to the station.", "The boss needs to be collected from the station.", "The boss doesn't know when the train arrives."],
          "answer": 1},
         {"q": "5. What does it say?", "image": IMG + "rq42_q.png",
          "options": ["Driver needed for five hours a week.", "Lifts available to community centre.", "Driver needed for retired people."],
          "answer": 0},
     ]},
    {"id": "r_p2", "type": "matching", "section": "reading", "part": 2, "start_num": 6,
     "question": "The people below are all looking for something to do this weekend.\nOn the opposite page there are descriptions of eight events.\nDecide which event would be the most suitable for the people below.",
     "instruction": "The people below are all looking for something to do this weekend.\nOn the opposite page there are descriptions of eight events.\nDecide which event would be the most suitable for the people below.",
     "events": EVENTS,
     "points": 5,
     "options": [
         "6. Ben has a teenage son who is taking exams at the end of the year. He would like an activity that his son can attend on Saturday to work on his art project.",
         "7. Tina wants to get her children outside this weekend to enjoy the sunshine. She'd like to find something that will keep them active so they use up some energy.",
         "8. Philip is looking after his ten-year-old nephew. He is looking for an activity on Sunday morning. He'd like something where he can sit down as he has a bad back.",
         "9. Tania is looking for something to do on either Saturday or Sunday evening. She and her friend Susan are taking their children. They would like somewhere they can listen to music and get something to eat.",
         "10. Anna and her husband Tom are visiting the area this weekend and would like to take their 12-year-old son. They would like to take their son somewhere on Saturday evening. They would prefer something that's not too expensive.",
     ],
     "option_images": [IMG + "p7_person6.png", IMG + "p7_person7.png", IMG + "p7_person8.png",
                       IMG + "p7_person9.png", IMG + "p7_person10.png"],
     "items": ["A Open Air Entertainment", "B Find Robert the Rabbit", "C Open Gardens",
               "D Tom and Larry's Garden Party", "E Mansfield Arts Market", "F Art Attack",
               "G Wanted: Young Musicians", "H Hassocks Green Festival"],
     "answer": [5, 1, 7, 3, 0]},
    {"id": "r_p3", "type": "multiple_group", "section": "reading", "part": 3, "start_num": 11,
     "question": "Look at the sentences below about a motorbike trip.\nRead the text to decide if each sentence is correct or incorrect.\nIf it is correct, write YES. If it is not correct, write NO.",
     "instruction": "Look at the sentences below about a motorbike trip.\nRead the text to decide if each sentence is correct or incorrect.\nIf it is correct, write YES. If it is not correct, write NO.",
     "title": "My first long motorbiking trip – by Graham Jones",
     "passage": MOTORBIKE_TEXT,
     "points": 5,
     "items": [
         {"q": "11. Luke was confident their first ride with his club would be a totally positive experience.",
          "options": ["YES", "NO"], "answer": 1},
         {"q": "12. For Graham's first group ride, they planned to go to a place 100 kilometres away.",
          "options": ["YES", "NO"], "answer": 1},
         {"q": "13. One rider in their group, Tania, started her bike without help when it broke down.",
          "options": ["YES", "NO"], "answer": 1},
         {"q": "14. Luke was concerned that the weather conditions were making their ride dangerous.",
          "options": ["YES", "NO"], "answer": 0},
         {"q": "15. Luke and Graham's mood improved after they reached Graham's house.",
          "options": ["YES", "NO"], "answer": 0},
     ]},
    {"id": "r_p4", "type": "multiple_group", "section": "reading", "part": 4, "start_num": 16,
     "question": "For each question, choose the correct answer.",
     "instruction": "For each question, choose the correct answer.",
     "title": "Robert Taylor talks about his new art show",
     "passage": ROBERT_TEXT,
     "points": 5,
     "items": [
         {"q": "16. What does Robert say about art?",
          "options": ["Children usually continue doing it at school.", "He had to give it up to do other subjects.", "The thought of showing off his work is a little frightening.", "He has often thought about letting people see his work."],
          "answer": 2},
         {"q": "17. When deciding what to study at university",
          "options": ["Robert didn't consider doing art.", "his parents didn't want him to study art.", "he thought he would need a job while he was studying.", "Robert understood correctly what his parents wanted him to do."],
          "answer": 0},
         {"q": "18. What happened while Robert was at university?",
          "options": ["He didn't do any painting.", "He discovered his love of painting again.", "He was still keen on art.", "He painted at least one evening a week."],
          "answer": 2},
         {"q": "19. Robert is holding the exhibition because",
          "options": ["his friends and relatives encouraged him to do this.", "the library asked him to.", "he is interested in getting opinions from friends and relatives.", "he wants to know what strangers think of his work."],
          "answer": 3},
         {"q": "20. What would be a good introduction to this article?",
          "options": ["Robert Taylor tells us how a love of art can lead to a change of career.", "If your child shows an interest in art, Robert Taylor will explain how to support this activity.", "After years in the shadows, Robert Taylor is about to face the public with his works.", "If you're keen on developing your artistic skills, Robert Taylor explains how to get support from friends and relatives."],
          "answer": 2},
     ]},
    {"id": "r_p5", "type": "multiple_group", "section": "reading", "part": 5, "start_num": 21,
     "question": "For each question, choose the correct answer.",
     "instruction": "For each question, choose the correct answer.",
     "title": "The Black Mamba",
     "inline_gaps": True,
     "passage": MAMBA_TEXT,
     "points": 5,
     "items": [
         {"q": "21. A bite from the Black Mamba is (21) ________ the 'kiss of death' in South Africa",
          "options": ["said", "made", "called", "titled"], "answer": 2},
         {"q": "22. and it is (22) ________ a very dangerous snake.",
          "options": ["certainly", "exactly", "just", "fairly"], "answer": 0},
         {"q": "23. The venom can kill a person within 30 minutes to a few hours (23) ________ medical help.",
          "options": ["outside", "besides", "away", "without"], "answer": 3},
         {"q": "24. though it uses this speed to (24) ________ danger rather than to attack.",
          "options": ["break", "escape", "lose", "run"], "answer": 1},
         {"q": "25. In fact, the Black Mamba is a rather (25) ________ creature and will avoid people if possible.",
          "options": ["shy", "brave", "afraid", "soft"], "answer": 0},
     ]},
]

WRITING_QUESTIONS = [
    {"id": "w1", "type": "writing", "section": "writing", "start_num": 1,
     "question": "Your class is organizing a cultural evening at school.\n\nWrite an email to your teacher, Mr. Williams.\n\nIn your email:\n• Invite him to attend\n• Explain why the event is special\n• Tell him what role he could play during the evening\n\nWrite at least 100 words.",
     "word_limit": "100", "points": 20},
]


def seed_b1plus_mid(db):
    """Insert or replace the B1+ MID test document."""
    test = {
        "section": "b1plus_mid",
        "title": "B1+ · MID",
        "icon": "📘",
        "time_limit": 70,
        "price": 0,
        "original_price": 0,
        "active": True,
        "description": "B1+ daraja oraliq imtihoni — Listening + Reading + Writing",
        "audio_parts": audio_parts,
        "created_at": datetime.now(timezone.utc),
        "questions": LISTENING_QUESTIONS + READING_QUESTIONS + WRITING_QUESTIONS,
    }
    db.tests.delete_many({"section": "b1plus_mid"})
    db.tests.insert_one(test)
    return len(test["questions"])
