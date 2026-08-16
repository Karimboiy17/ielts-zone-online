"""Auto-seed NOVICE MID test data into MongoDB (used at app startup on Railway)."""
from datetime import datetime, timezone

AUDIO = "/static/audio/novice_mid_listening_full.mp3"
IMG = "/static/images/novice_mid/"

# ============ READING PASSAGE 1 ============
SLEEPING_TEXT = """Can curling up under your desk, or in a purpose-built sleep pod, for a 10-minute sleep improve your performance at work?

There are times, typically in the afternoon, when many office workers experience a feeling of tiredness and may even drift off to sleep in front of their computers. Many workplaces consider artificial stimulation, provided by coffee or a chocolate bar, more acceptable than a short sleep when attempting to combat this daytime sleepiness. However, there is considerable evidence that trying to work during a spell of daytime drowsiness can be costly.

'Workplace accidents and errors peak at the same time that our circadian rhythms (sleep-wake cycle) cause a drop in alertness,' says Dr Gerard Kennedy, a sleep specialist based in Melbourne, Australia. 'That's between about two and five pm,' he says. These biologically based downturns in alertness are natural and occur even if you've had a good night's sleep. Most workers simply continue during the after-lunch decline or reach for the nearest energiser: a strong coffee, a can of high-caffeine soft drink, a cigarette or some secretly stored chocolate in the top drawer.

However, a growing number of workers are taking very short sleeps, or 'power naps' instead. 'Research shows that a nap can improve your mood and productivity, alleviate tiredness, increase alertness and reduce errors at work,' says Kennedy. 'A nap as brief as 10 minutes will produce these results.' It seems that the length of the nap is significant. Professor Leon Lack, from the School of Psychology at Adelaide's Flinders University, has compared 5-, 10-, 20- and 30-minute naps; he measured sleepiness, reaction time and cognitive performance before and immediately after a nap and again during the next three hours. 'The 5-minute nap delivered very few benefits,' says Lack. 'The 20- and 30-minute naps produced improvements but the subjects took at least half an hour to wake up completely.' Lack explains that the longer the sleep, the deeper it is, which can lead to a feeling called sleep inertia. 'The 10-minute nap delivered immediate benefits that lasted for two to three hours, including a small but significant increase in alertness.'

But how can just 10 minutes of sleep be ensured, when not in lab conditions? Most people take 5 to 10 minutes to fall asleep so they need to lie down for a total of 20 minutes to allow for 10 to 15 minutes of sleep. First, we need to change our attitudes to rest.

Australians work an average of 1811 hours each year, according to 2005 figures from the Organisation for Economic Co-operation and Development (OECD). This is the fifth highest figure from 26 nations surveyed. In addition, Dr Kennedy stated that 9% of 20- to 30-year-olds and 16% of 30- to 50-year-olds are reporting sleeping problems. But in Australia, a culture where doing anything at all is considered better than doing nothing, lying down for a while - in the face of deadlines and urgent requests - is regarded as unacceptable by most companies. Some companies, however, are listening to experts who advise on ways to help employees take quick naps.

Both low- and high-tech napping methods are available for those who want to try. Low-tech napping can include the use of a basic relaxation room or, in the case of the strategic public relations firm Wordplay, a 'CushoBed'. This combination of a very large cushion and a couch provides Wordplay's staff with a comfortable place to curl up for a short sleep. Then there's the high-tech 'TechnoSnooze', an up-market sleeping pod that arrived in Australia from New York earlier this year, and which has been leased out to several companies on trial, including advertising agencies State Right Australia and Instant Publicity. Looking like a space-age reclining armchair, the TechnoSnooze has a rounded hood that lowers over the head and headphones that play relaxation music. The pod inclines forward to allow for easy entry, then reclines so that the user's feet are slightly elevated. This promotes blood circulation and reduces pressure on the lower back. After 20 minutes, the pod vibrates gently to wake you.

Harry Baker, the managing director of another large company, doesn't need such a high-tech approach. He makes good use of his media company's meditation room, which includes quiet music, candles, and incense. He encourages his staff to use it too. 'Napping is a good idea,' says Baker. 'It's like a traffic signal that slows down your brain.'

However, employees need strong workplace support from their bosses and co-workers to feel they have permission for a mini-sleep as a regular part of their working day. 'Workplace napping made a huge amount of sense to me very quickly, and I assumed the idea would sell itself, but that wasn't always the case,' says Kevin Hopkins from State Right Australia, which trialled pod-style napping for a month. 'For napping to be beneficial, you need to ensure good briefing of the managers so they are clear about the positive outcomes and are equipped to endorse, role-model, and support staff, since staff will usually take their lead from managers.' He says staff response was positive: 43% of those who booked themselves in for a pod nap said they felt 'good' and 21% 'excellent' afterwards."""

# ============ READING PASSAGE 2 ============
JETLAG_TEXT = """A. We like to think we have control over our bodies, but the opposite is often true. Such is the case with 'circadian desynchrony', a condition more commonly known as jet lag. Exhaustion, headaches, difficulty concentrating, light-headedness, trouble falling asleep or staying asleep; these are common effects of jet lag. They have the power to ruin a vacation or business trip unless you learn how to trick your own body.

B. Experimental psychologist John Caldwell has spent most of his career researching the effects of sleep deprivation and sleep restriction, while also studying countermeasures that sleep-deprived people can use to function better. Much of his research was conducted within the military community. Caldwell explains that while our bodies are able to adjust to about one time zone change per day, jet lag sets in when we cross three or more of them because it creates chaos in circadian rhythms (otherwise known as our body clock). That's a fairly new phenomenon, historically speaking. 'People now can fly from New York to Paris in nine hours, whereas in 1923 you did it on a ship and it took you six days to get over to Europe,' Caldwell says. 'We just haven't evolved to the point where we can rapidly change those rhythms, because it's a relatively recent thing.'

C. Because of the problems your body has naturally adapting to time-zone changes, you need to manually adjust your body clock, and that means changing your bedtime to be better matched with the destination to which you're traveling. Ranit Mishori, a professor of family medicine at Georgetown University School of Medicine, travels frequently to Europe, Africa, and the Middle East. To be ready to work when she arrives, she starts adjusting her bedtime two to five days in advance to match the local time at her destination. 'That means going to bed earlier when going east and waking up much earlier,' she says. When she returns to the US, she does the same but in reverse. John Caldwell creates a timetable that includes meetings, bedtimes, and social activities so that he can easily see what time it is at home and at his destination and plan accordingly. 'A lot of times, when you look at that table, right away you're going to see where you're going to have your biggest problems,' he says. If he's just traveling for a quick business trip and will only be gone a couple of days, he avoids gradual adjustment. Instead, he tries to schedule any meetings at a time when he would be awake and focused back home.

D. Circadian rhythms are influenced by natural light. While travel may disrupt those rhythms, you can help get them back on track by regulating the amount of light that your body encounters, says Pradeep Bollu, associate director of University of Missouri Health Care Sleep Disorders Center. When traveling east, your biological clock will be behind: '... avoiding bright light in the evening can help with advancing our biological clock,' he says. 'Similarly, bright light ... after waking up also will help advance our biological clock to suit the new time zone.' When traveling westward, he adds, the biological clock is ahead of the destination time. He suggests gravitating toward bright light in the evening, if possible, and exercising to stay awake later and sleep longer.

E. One suggestion that is sometimes made is taking the hormone melatonin, which is a substance that is produced every night by the human body and helps you sleep. 'Taking a very small dose helps to recalibrate its release so that it is in sync with the time zone of your destination,' says Kern Singh, a spine surgeon in Chicago with Midwest Orthopaedics at Rush. Singh says he takes five milligrams of melatonin - which you can buy in pill form in supermarkets and many main-street stores in the US - on the plane and then again when he lands.

F. Having a glass of wine on the plane may sound tempting, but it could negatively impact your sleep, which would worsen jet lag, says Quay Snyder, president and CEO of Aviation Medicine Advisory Service of Centennial, who advises pilots on staying in top condition while in the air. 'It definitely has a sedating effect as far as getting someone to sleep, but it destroys their rapid eye movement (REM) sleep so their actual mental recovery is reduced,' he says. Instead, he says, be sure and have plenty of water so that you stay hydrated while traveling.

G. Bruce Stephen Rashbaum, owner and medical director of Capital Center for Travel and Tropical Medicine in the District of Columbia, regularly advises patients on jet lag. He considers prednisone, which is a powerful prescription medication, to be the most effective tool for jet lag recovery. He instructs patients to take the medication when they land, which is typically early in the morning, and again in the late afternoon and the next day. 'It is this simple ritual that works nearly every time,' he says. So if in doubt, you can always ask your doctor for some assistance.

Everyone responds to jet lag differently. For those who suffer, the first week will be the most challenging, but after that, your body should start to recover."""

questions = [
    # ============ LISTENING Part 1 (Q1-12): table completion ============
    {"id": "l_p1", "type": "writing", "section": "listening", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-12.\nComplete the tables below.\nWrite ONE WORD AND/OR A NUMBER for each answer.",
     "title": "Accommodation in Framlington",
     "passage": ("Accommodation in Framlington\n\n"
                 "• The Loft — apartment — near the (1) ________. It has a view of the (2) ________.\n"
                 "• Tim's Place — (3) ________ — on (4) ________ Street. A maximum of (5) ________ people can stay.\n"
                 "• The (6) ________ — apartment — in a great place for watching (7) ________. The building has a lot of (8) ________.\n\n"
                 "Things to do in Framlington\n\n"
                 "• Cycle tour — bike and helmet provided — Cycle by a (9) ________ out of Framlington. Visit a village famous for its (10) ________. Go through the country's longest (11) ________ for bikes.\n"
                 "• Photo tour — a camera with flash — See the best places to photograph Framlington's (12) ________."),
     "gap_items": ["Station", "Castle", "Boat", "Bridge", "(6) six", "Zooshie", "Birds",
                   "Stairs", "Canal", "Cheese", "Tunnel", "Monuments"],
     "gap_labels": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
     "points": 12},

    # ============ LISTENING Part 2 (Q13-19): MC Diamond Creek Dinosaur Park ============
    {"id": "l_p2", "type": "multiple_group", "section": "listening", "part": 2, "start_num": 13,
     "instruction": "Part 2. Questions 13-19.\nYou will hear a talk about the Diamond Creek Dinosaur Park.\nFor each question, choose the correct letter, A, B or C.",
     "points": 7,
     "items": [
         {"q": "13. What does the speaker say about the land on which the Dinosaur Park is located?",
          "options": ["It had an important train line on it.", "It was once a farming area.", "It used to be covered in trees."],
          "answer": 2},
         {"q": "14. The dinosaur bones in the park",
          "options": ["came from one kind of dinosaur.", "were found by accident.", "are in very good condition."],
          "answer": 1},
         {"q": "15. What does the speaker say about the museum building?",
          "options": ["It won an architecture award.", "It has an interesting design feature.", "It was surprisingly cheap to build."],
          "answer": 1},
         {"q": "16. The ticket to the museum includes",
          "options": ["access to all areas.", "a detailed guidebook.", "a talk by a dinosaur expert."],
          "answer": 2},
         {"q": "17. Some of the walking tracks through the park",
          "options": ["are difficult to follow.", "go up and down hills.", "need to be repaired."],
          "answer": 0},
         {"q": "18. What does the speaker say about Dinosaur Crater?",
          "options": ["It is unsuitable for children.", "It is best to visit in the late afternoon.", "It can be reached on foot."],
          "answer": 1},
         {"q": "19. Where does the speaker say dinner will be held tonight?",
          "options": ["in a restaurant in the nearby town.", "in the museum café.", "in an outdoor eating area."],
          "answer": 2},
     ]},

    # ============ LISTENING Part 3 (Q20-25): map labelling ============
    {"id": "l_p3", "type": "matching", "section": "listening", "part": 3, "start_num": 20,
     "instruction": "Questions 20-25.\nLabel the map below.\nWrite the correct letter, A-I, next to questions 20-25.",
     "passage": '<img src="' + IMG + 'map.png" alt="Dinosaur Park map" style="max-width:100%;height:auto;border-radius:8px;">',
     "points": 6,
     "options": [
         "20. Dinosaur Canyon Exhibit",
         "21. Dinosaur Stampede Exhibit",
         "22. Dinosaur Discovery Area",
         "23. Picnic area",
         "24. Water station",
         "25. Toilets",
     ],
     "items": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
     "answer": [3, 7, 2, 8, 0, 6]},

    # ============ READING Part 1 (Q1-4): True/False/Not Given ============
    {"id": "r_p1", "type": "multiple_group", "section": "reading", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-4.\nDo the following statements agree with the information given in the passage?\nWrite TRUE if the statement agrees, FALSE if it contradicts, NOT GIVEN if there is no information.",
     "title": "Sleeping on the Job",
     "passage": SLEEPING_TEXT,
     "points": 4,
     "items": [
         {"q": "1. The majority of mistakes in the workplace happen in the afternoon.",
          "options": ["True", "False", "Not Given"], "answer": 0},
         {"q": "2. A short nap of five minutes is enough to reduce errors at work.",
          "options": ["True", "False", "Not Given"], "answer": 1},
         {"q": "3. People who work long hours are more likely to have sleeping problems.",
          "options": ["True", "False", "Not Given"], "answer": 2},
         {"q": "4. Doing nothing is acceptable in Australian culture.",
          "options": ["True", "False", "Not Given"], "answer": 1},
     ]},

    # ============ READING Part 2 (Q5-10): table completion ============
    {"id": "r_p2", "type": "writing", "section": "reading", "part": 2, "start_num": 5,
     "instruction": "Part 2. Questions 5-10.\nComplete the table below using the passage 'Sleeping on the Job'.\nChoose NO MORE THAN TWO WORDS AND/OR A NUMBER from the passage for each answer.",
     "title": "Where naps take place",
     "passage": ("CushoBed — Wordplay — Blends features of a giant (5) ________ and a sofa.\n\n"
                 "TechnoSnooze — State Right Australia / Instant Publicity — An ultra-modern lounger with a (6) ________ at the top. Lessens stress on the (7) ________. Allows you to sleep for a maximum of (8) ________.\n\n"
                 "(9) ________ — Harry Baker — A sweet-smelling room with subtle lighting and background (10) ________."),
     "gap_items": ["Cushion", "Rounded hood", "Lower back", "20 minutes", "Meditation room", "Music"],
     "gap_labels": ["5", "6", "7", "8", "9", "10"],
     "points": 6},

    # ============ READING Part 3 (Q11-13): short answer ============
    {"id": "r_p3", "type": "writing", "section": "reading", "part": 3, "start_num": 11,
     "instruction": "Part 3. Questions 11-13.\nAnswer the questions below using the passage 'Sleeping on the Job'.\nChoose NO MORE THAN THREE WORDS from the passage for each answer.",
     "title": "Short answer questions",
     "passage": ("11. To what does Harry Baker compare napping?\nAnswer: (11) ________\n\n"
                 "12. Apart from their superiors, who do workers need consent from if they are to feel comfortable taking a nap at work?\nAnswer: (12) ________\n\n"
                 "13. What do managers need to understand before they can support their staff in 'sleeping on the job'?\nAnswer: (13) ________"),
     "gap_items": ["Traffic signal", "Co-workers", "Positive outcomes"],
     "gap_labels": ["11", "12", "13"],
     "points": 3},

    # ============ READING Part 4 (Q14-19): matching headings ============
    {"id": "r_p4", "type": "matching", "section": "reading", "part": 4, "start_num": 14,
     "instruction": "Part 4. Questions 14-19.\nThe passage has seven paragraphs, A-G.\nChoose the correct heading for each paragraph from the list of headings below.\nWrite the correct number, i-ix. (Paragraph A is given as an example: iv.)",
     "title": "Reducing the effects of jet lag",
     "passage": JETLAG_TEXT,
     "points": 6,
     "options": [
         "14. Paragraph B",
         "15. Paragraph C",
         "16. Paragraph D",
         "17. Paragraph E",
         "18. Paragraph F",
         "19. Paragraph G",
     ],
     "items": [
         "i Requesting help from professionals",
         "ii Types of meals and beverages that help",
         "iii What not to do on a flight",
         "iv Symptoms of jet lag",
         "v Altering your sleep schedules",
         "vi Types of exercise to do",
         "vii A problem of the modern age",
         "viii A remedy available from ordinary shops",
         "ix Timing exposure to sunshine",
     ],
     "answer": [6, 4, 8, 7, 2, 0]},

    # ============ READING Part 5 (Q20-22): matching statements to experts ============
    {"id": "r_p5", "type": "matching", "section": "reading", "part": 5, "start_num": 20,
     "instruction": "Part 5. Questions 20-22.\nLook at the following statements and the list of experts below.\nMatch each statement with the correct expert, A-F.",
     "points": 3,
     "options": [
         "20. Using strong medicine is the most efficient way to get over jet lag.",
         "21. Using natural supplements to reset biological processes can help travelers.",
         "22. Having certain types of drinks lessens the quality of sleep.",
     ],
     "items": ["A John Caldwell", "B Ranit Mishori", "C Pradeep Bollu",
               "D Kern Singh", "E Quay Snyder", "F Bruce Stephen Rashbaum"],
     "answer": [5, 3, 4]},

    # ============ READING Part 6 (Q23-25): summary completion ============
    {"id": "r_p6", "type": "writing", "section": "reading", "part": 6, "start_num": 23,
     "instruction": "Part 6. Questions 23-25.\nComplete the summary below using the passage 'Reducing the effects of jet lag'.\nChoose ONE WORD ONLY from the passage for each answer.",
     "title": "Why we experience jet lag",
     "passage": ("John Caldwell has studied sleep issues among (23) ________ personnel. He explains that jet lag is an issue because the human body can only naturally adapt to one change in time zones per day; traveling over more than that causes (24) ________ for our bodies. Unlike when traveling by (25) ________, flying has resulted in us being able to change many time zones quickly. As this is a fairly new form of travel, the human body hasn't yet evolved to be able to cope with this."),
     "gap_items": ["Military", "Chaos", "Ship"],
     "gap_labels": ["23", "24", "25"],
     "points": 3},

    # ============ WRITING ============
    {"id": "w1", "type": "writing", "section": "writing", "start_num": 1,
     "question": ("The graph below shows the percentage of female members of parliament in five European countries, from 2000 to 2012.\n\n"
                  "Summarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\n"
                  "Write at least 150 words."),
     "image": IMG + "writing_graph.png",
     "word_limit": "150", "points": 20},
]

test = {
    "section": "novice_mid",
    "title": "🌱 NOVICE · MID",
    "icon": "🌱",
    "time_limit": 55,
    "price": 0,
    "original_price": 0,
    "active": True,
    "description": "Novice daraja oraliq imtihoni — Listening + Reading + Writing",
    "audio_parts": [AUDIO, AUDIO, AUDIO, AUDIO],
    "created_at": datetime.now(timezone.utc),
    "questions": questions,
}


def seed_novice_mid(db):
    """Insert or update the NOVICE MID test document (keeps _id stable so old attempts work)."""
    db.tests.update_one(
        {"section": "novice_mid"},
        {"$set": test},
        upsert=True,
    )
    return len(test["questions"])
