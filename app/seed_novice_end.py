"""Auto-seed NOVICE END test data into MongoDB (used at app startup on Railway).

Listening 40 savol (4 part) + Reading 40 savol (3 passage) + Writing 2 task.
Jami 82 savol. Har bir savol javoblar kaliti bo'yicha to'g'ri index'ga moslangan.
"""
from datetime import datetime, timezone

AUDIO = "/static/audio/novice_end_listening_full.mp3"
IMG = "/static/images/novice_end/"

# ============ READING PASSAGE TEXTS ============

KAMKWAMBA_TEXT = """At only 14 years old, William Kamkwamba built a series of windmills that could generate electricity in his African village, Masitala, in Malawi, south-eastern Africa.

In 2002, William Kamkwamba had to drop out of school, as his father, a maize and tobacco farmer, could no longer afford his school fees. But despite this setback, William was determined to get his education. He began visiting a local library that had just opened in his old primary school, where he discovered a tattered science book. With only a rudimentary grasp of English, he taught himself basic physics – mainly by studying photos and diagrams. Another book he found there featured windmills on the cover and inspired him to try and build his own.

He started by constructing a small model. Then, with the help of a cousin and friend, he spent many weeks searching scrap yards and found old tractor fans, shock absorbers, plastic pipe and bicycle parts, which he used to build the real thing.

For windmill blades, William cut some bath pipe in two lengthwise, then heated the pieces over hot coals to press the curled edges flat. To bore holes into the blades, he stuck a nail through half a corncob, heated the metal red and twisted it through the blades. It took three hours to repeatedly heat the nail and bore the holes. He attached the blades to a tractor fan using proper nuts and bolts and then to the back axle of a bicycle. Electricity was generated through the bicycle dynamo. When the wind blew the blades, the bike spun the bike wheel, which charged the dynamo and sent a current through wire to his house.

What he had built was a crude machine that produced 12 volts and powered four lights. When it was all done, the windmill's wingspan measured more than eight feet and sat on top of a rickety tower 15 feet tall that swayed violently in strong gales. He eventually replaced the tower with a sturdier one that stands 39 feet, and built a second machine that watered a family garden.

The windmill brought William Kamkwamba instant local fame, but despite his accomplishment, he was still unable to return to school. However, news of his magetsi a mphepo – electric wind – spread beyond Malawi, and eventually things began to change. An education official, who had heard news of the windmill, came to visit his village and was amazed to learn that William had been out of school for five years. He arranged for him to attend secondary school at the government's expense and brought journalists to the farm to see the windmill. Then a story published in the Malawi Daily Mail caught the attention of bloggers, which in turn caught the attention of organisers for the Technology Entertainment and Design conference.

In 2007, William spoke at the TED Global conference in Tanzania and got a standing ovation. Businessmen stepped forward with offers to fund his education and projects, and with money donated by them, he was able to put his cousin and several friends back into school and pay for some medical needs of his family. With the donation, he also drilled a borehole for a well and water pump in his village and installed drip irrigation in his father's fields.

The water pump has allowed his family to expand its crops. They have abandoned tobacco and now grow maize, beans, soybeans, potatoes and peanuts. The windmills have also brought big lifestyle and health changes to the other villagers. 'The village has changed a lot,' William says. 'Now, the time that they would have spent going to fetch water, they are using for doing other things. And also the water they are drinking is clean water, so there is less disease.' The villagers have also stopped using kerosene and can use the money previously spent on fuel to buy other things.

William Kamkwamba's example has inspired other children in the village to pursue science. William says they now see that if they put their mind to something, they can achieve it. 'It has changed the way people think,' he says."""

CHAMONIX_TEXT = """A  The town of Chamonix-Mont-Blanc sits in a valley at 1,035 metres above sea level in the Haute-Savoie department in south-eastern France. To the north-west are the red peaks of the Aiguilles Rouges massif; to the south-east are the permanently white peaks of Mont Blanc, which at 4,810 metres is the highest mountain in the Alps. It's a typical Alpine environment, but one that is under increasing strain from the hustle and bustle of human activity.

B  Tourism is Chamonix's lifeblood. Visitors have been encouraged to visit the valley ever since it was discovered by explorers in 1741. Over 40 years later, in 1786, Mont Blanc's summit was finally reached by a French doctor and his guide, and this gave birth to the sport of alpinism, with Chamonix at its centre. In 1924, it hosted the first Winter Olympics, and the cable cars and lifts that were built in the years that followed gave everyone access to the ski slopes.

C  Today, Chamonix is a modern town, connected to the outside world via the Mont Blanc Road Tunnel and a busy highway network. It receives up to 60,000 visitors at a time during the ski season, and climbers, hikers and extreme-sports enthusiasts swarm there in the summer in even greater numbers, swelling the town's population to 100,000. It is the third most visited natural site in the world, according to Chamonix's Tourism Office, and last year, it had 5.2 million visitor bed nights – all this in a town with fewer than 10,000 permanent inhabitants.

D  This influx of tourists has put the local environment under severe pressure, and the authorities in the valley have decided to take action. Educating visitors is vital. Tourists are warned not to drop rubbish, and there are now recycling points dotted all around the valley, from the town centre to halfway up the mountains. An internet blog reports environmental news in the town, and the 'green' message is delivered with all the tourist office's activities.

E  Low-carbon initiatives are also important for the region. France is committed to reducing its carbon emissions by a factor of four by 2050. Central to achieving this aim is a strategy that encourages communities to identify their carbon emissions on a local level and make plans to reduce them. Studies have identified that accommodation accounts for half of all carbon emissions in the Chamonix valley. Hotels are known to be inefficient operations, but those around Chamonix are now cleaning up their act. Some are using low-energy lighting, restricting water use and making recycling bins available for guests; others have invested in huge projects such as furnishing and decorating using locally sourced materials, using geothermal energy for heating and installing solar panels.

F  Chamonix's council is encouraging the use of renewable energy in private properties too, by making funds available for green renovations and new constructions. At the same time, public-sector buildings have also undergone improvements to make them more energy efficient and less wasteful. For example, the local ice rink has reduced its annual water consumption from 140,000 cubic metres to 10,000 cubic metres in the space of three years.

G  Improving public transport is another feature of the new policy, as 80 percent of carbon emissions from transport used to come from private vehicles. While the Mont Blanc Express is an ideal way to travel within the valley — and see some incredible scenery along the route — it is much more difficult to arrive in Chamonix from outside by rail. There is no direct line from the closest airport in Geneva, so tourists arriving by air normally transfer by car or bus. However, at a cost of 3.3 million euros a year, Chamonix has introduced a free shuttle service in order to get people out of their cars and into buses fitted with particle filters.

H  If the valley's visitors and residents want to know why they need to reduce their environmental impact, they just have to look up; the effects of climate change are there for everyone to see in the melting glaciers that cling to the mountains. The fragility of the Alpine environment has long been a concern among local people. Today, 70 percent of the 805 square kilometres that comprise Chamonix-Mont-Blanc is protected in some way. But now, the impact of tourism has led the authorities to recognise that more must be done if the valley is to remain prosperous: that they must not only protect the natural environment better, but also manage the numbers of visitors better, so that its residents can happily remain there."""

SCREEN_TEXT = """Reading and writing, like all technologies, are constantly changing. In ancient times, authors often dictated their books. Dictation sounded like an uninterrupted series of words, so scribes wrote these down in one long continuous string, just as they occur in speech. For this reason, text was written without spaces between words until the 11th century. This continuous script made books hard to read, so only a few people were accomplished at reading them aloud to others. Being able to read silently to yourself was considered an amazing talent; writing was an even rarer skill. In fact, in 15th-century Europe, only one in 20 adult males could write.

After Gutenberg's invention of the printing press in about 1440, mass-produced books changed the way people read and wrote. The technology of printing increased the number of words available, and more types of media, such as newspapers and magazines, broadened what was written about. Authors no longer had to produce scholarly works, as was common until then, but could write, for example, inexpensive, heart-rending love stories or publish autobiographies, even if they were unknown.

In time, the power of the written word gave birth to the idea of authority and expertise. Laws were compiled into official documents, contracts were written down and nothing was valid unless it was in this form. Painting, music, architecture, dance were all important, but the heartbeat of many cultures was the turning pages of a book. By the early 19th century, public libraries had been built in many cities.

Today, words are migrating from paper to computers, phones, laptops and game consoles. Some 4.5 billion digital screens illuminate our lives. Letters are no longer fixed in black ink on paper, but flitter on a glass surface in a rainbow of colors as fast as our eyes can blink. Screens fill our pockets, briefcases, cars, living-room walls and the sides of buildings. They sit in front of us when we work – regardless of what we do. And of course, these newly ubiquitous screens have changed how we read and write.

The first screens that overtook culture, several decades ago – the big, fat, warm tubes of television – reduced the time we spent reading to such an extent that it seemed as if reading and writing were over. Educators and parents worried deeply that the TV generation would be unable to write. But the interconnected, cool, thin displays of computer screens launched an epidemic of writing that continues to swell. As a consequence, the amount of time people spend reading has almost tripled since 1980. By 2008, the World Wide Web contained more than a trillion pages, and that total grows rapidly every day.

But it is not book reading or newspaper reading, it is screen reading. Screens are always on, and, unlike books, we never stop staring at them. This new platform is very visual, and it is gradually merging words with moving images. You might think of this new medium as books we watch, or television we read. We also use screens to present data, and this encourages numeracy: visualising data and reading charts, looking at pictures and symbols are all part of this new literacy.

Screens engage our bodies, too. The most we may do while reading a book is to flip the pages or turn over a corner, but when we use a screen, we interact with what we see. In the futuristic movie Minority Report, the main character stands in front of a screen and hunts through huge amounts of information as if conducting an orchestra. Just as it seemed strange five centuries ago to see someone read silently, in the future it will seem strange to read without moving your body.

In addition, screens encourage more utilitarian (practical) thinking. A new idea or unfamiliar fact will cause a reflex to do something: to research a word, to question your screen 'friends' for their opinions or to find alternative views. Book reading strengthened our analytical skills, encouraging us to think carefully about how we feel. Screen reading, on the other hand, encourages quick responses, associating this idea with another, equipping us to deal with the thousands of new thoughts expressed every day. For example, we review a movie for our friends while we watch it; we read the owner's manual of a device we see in a shop before we purchase it, rather than after we get home and discover that it can't do what we need it to do.

Screens provoke action instead of persuasion. Propaganda is less effective, and false information is hard to deliver in a world of screens because while misinformation travels fast, corrections do, too. On a screen, it is often easier to correct a falsehood than to tell one in the first place. Wikipedia works so well because it removes an error in a single click. In books, we find a revealed truth; on the screen, we assemble our own truth from pieces.

What is more, a screen can reveal the inner nature of things. Waving the camera eye of a smartphone over the bar code of a manufactured product reveals its price, origins and even relevant comments by other owners. It is as if the screen displays the object's intangible essence. A popular children's toy (Webkinz) instills stuffed animals with a virtual character that is 'hidden' inside; a screen enables children to play with this inner character online in a virtual world.

In the near future, screens will be the first place we'll look for answers, for friends, for news, for meaning, for our sense of who we are and who we can be."""

# ============ LISTENING ============

LISTENING_QUESTIONS = [
    # Part 1 (Q1-10): form completion (gap-fill)
    {"id": "l_p1", "type": "writing", "section": "listening", "part": 1, "start_num": 1,
     "instruction": "Part 1. Questions 1-10.\nComplete the form below.\nWrite NO MORE THAN ONE WORD AND/OR A NUMBER for each answer.",
     "title": "HOTEL BOOKING FORM",
     "passage": "Arrival date: 23rd August (example)\nLength of stay: (1) ________\nType of accommodation: (2) ________ room\nName: Mr and Mrs (3) ________ and children\nAddress: 29 Tower Heights, Dunbar, (4) ________\nPostcode: EH41 2GK\nContact telephone: (5) ________\nPurpose of trip: holiday\n\nTOURIST BOARD — Questions for holidaymakers\nFavourite activity: (6) ________\nBeaches: busy but (7) ________\nShop staff: are sometimes overly (8) ________\nWaiters: (9) ________ and quick\nSuggestions: need some (10) ________ for hire",
     "gap_items": ["TWO WEEKS", "FAMILY", "SHRIVER", "SCOTLAND", "0131 9946 5723",
                   "SWIMMING", "CLEAN", "HELPFUL", "POLITE", "BIKES"],
     "gap_labels": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
     "points": 10},

    # Part 2 (Q11-15): notes completion (gap-fill)
    {"id": "l_p2", "type": "writing", "section": "listening", "part": 2, "start_num": 11,
     "instruction": "Part 2. Questions 11-15.\nComplete the notes below.\nWrite NO MORE THAN ONE WORD AND/OR A NUMBER for each answer.",
     "title": "ORANA WILDLIFE PARK",
     "passage": "Facts about Orana\n• Orana means '(11) ________'.\n• The park has animals from a total of (12) ________.\n• The animals come from many parts of the world.\n\nThings to do at Orana\n• (13) ________ the giraffes at 12 or 3 p.m.\n• Touch the animals in the (14) ________ (good for children).\n• Watch the cheetahs doing their running (15) ________ at 3.40.",
     "gap_items": ["WELCOME", "70 SPECIES", "HAND-FEED", "FARMYARD", "EXERCISE"],
     "gap_labels": ["11", "12", "13", "14", "15"],
     "points": 5},

    # Part 2 (Q16-20): label the plan (matching A-I)
    {"id": "l_p2b", "type": "matching", "section": "listening", "part": 3, "start_num": 16,
     "instruction": "Part 2. Questions 16-20.\nLabel the plan below.\nWrite the correct letter, A-I, next to questions 16-20.",
     "points": 5,
     "options": [
         "16. New Zealand birds",
         "17. African village",
         "18. Picnic area",
         "19. Afternoon walkabout meeting place",
         "20. Jomo's Café",
     ],
     "items": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
     "answer": [1, 6, 4, 2, 7]},

    # Part 3 (Q21-27): MC
    {"id": "l_p3", "type": "multiple_group", "section": "listening", "part": 4, "start_num": 21,
     "instruction": "Part 3. Questions 21-27.\nChoose the correct letter A, B or C.",
     "points": 7,
     "items": [
         {"q": "21. The students did the study skills course because",
          "options": ["it was part of their syllabus.", "they needed it to prepare for an exam.", "their tutor recommended it."],
          "answer": 2},
         {"q": "22. Why did Sylvie and Daniel use a questionnaire?",
          "options": ["Other students preferred the method.", "It reduced the preparation time.", "More information could be obtained."],
          "answer": 1},
         {"q": "23. How often did the students meet in class for the course?",
          "options": ["once a week", "twice a week", "every weekday"],
          "answer": 0},
         {"q": "24. Why did Daniel like the course?",
          "options": ["It improved his confidence.", "It focused on economics articles.", "It encouraged him to read more books."],
          "answer": 0},
         {"q": "25. What did the students like about Jenny?",
          "options": ["her homework assignments", "her choice of study material", "her style of teaching"],
          "answer": 1},
         {"q": "26. Which chart below shows how useful students found the course in general?",
          "options": ["A", "B", "C"], "answer": 2},
         {"q": "27. Which graph below shows how useful students found the different parts of the course?",
          "options": ["A", "B", "C"], "answer": 1},
     ]},

    # Part 3 (Q28-30): sentence completion (gap-fill)
    {"id": "l_p3b", "type": "writing", "section": "listening", "part": 5, "start_num": 28,
     "instruction": "Part 3. Questions 28-30.\nComplete the sentences.\nUse NO MORE THAN ONE WORD for each answer.",
     "passage": "Good note-taking improves concentration during (28) ________.\nMaking notes with the help of a (29) ________ is useful.\nHaving a broad (30) ________ on note paper makes notes easier to read.",
     "gap_items": ["LECTURES", "DIAGRAM", "MARGIN"],
     "gap_labels": ["28", "29", "30"],
     "points": 3},

    # Part 4 (Q31-40): notes completion (gap-fill)
    {"id": "l_p4", "type": "writing", "section": "listening", "part": 6, "start_num": 31,
     "instruction": "Part 4. Questions 31-40.\nComplete the notes below.\nWrite NO MORE THAN ONE WORD for each answer.",
     "title": "AIRPORT DESIGN",
     "passage": "• Can compare a past airport to a (31) ________ station\n• Now, can compare an airport to a small (32) ________\n\nReasons for changes\n• Greater passenger numbers because of:\n  o (33) ________ large-scale (e.g., package deals)\n  o (34) ________ global (e.g., meetings)\n• Need to create a good (35) ________ of a country\n  o airports called 'gateways'\n\nTypes of change\nInside the building\n• Many big (36) ________ provide space and light (e.g., Beijing airport)\n• Calm atmosphere with easy movement reduces (37) ________ for passengers\n\nThe exterior of the building\n• Designed to match the surroundings\n  o e.g. the shape of the (38) ________ on the Arctic Circle airport, Norway\n  o the (39) ________ outside airports in India and Thailand\n• Structural design reduces (40) ________ and costs",
     "gap_items": ["BUS", "CITY", "TOURISM", "BUSINESS", "IMPRESSION", "AREAS", "STRESS", "ROOF", "GARDENS", "ENERGY"],
     "gap_labels": ["31", "32", "33", "34", "35", "36", "37", "38", "39", "40"],
     "points": 10},
]

# ============ READING ============

READING_QUESTIONS = [
    # Passage 1 — William Kamkwamba (Q1-13)
    {"id": "r_p1", "type": "writing", "section": "reading", "part": 1, "start_num": 1,
     "instruction": "READING PASSAGE 1. Questions 1-5.\nComplete the flow chart below.\nChoose NO MORE THAN TWO WORDS from the passage for each answer.",
     "title": "William Kamkwamba",
     "passage": KAMKWAMBA_TEXT + "\n\nBuilding the Windmill\nWilliam learned some (1) ________ from a library book.\nFirst, he built a (2) ________ of the windmill.\nThen he collected materials from (3) ________ with a relative.\nHe made the windmill blades from pieces of (4) ________.\nHe fixed the blades to a (5) ________ and then to part of a bicycle.\nHe raised the blades on a tower.",
     "gap_items": ["(BASIC) PHYSICS", "(SMALL) MODEL", "SCRAP YARDS", "(BATH) PIPE", "TRACTOR FAN"],
     "gap_labels": ["1", "2", "3", "4", "5"],
     "points": 5},

    # Passage 1 — True/False/Not Given (Q6-10)
    {"id": "r_p2", "type": "multiple_group", "section": "reading", "part": 2, "start_num": 6,
     "instruction": "Questions 6-10.\nDo the following statements agree with the information given in Reading Passage 1?\nTRUE if the statement agrees with the information\nFALSE if the statement contradicts the information\nNOT GIVEN if there is no information on this",
     "points": 5,
     "items": [
         {"q": "6. William used the electricity he created for village transport.",
          "options": ["True", "False", "Not Given"], "answer": 1},
         {"q": "7. At first, William's achievement was ignored by local people.",
          "options": ["True", "False", "Not Given"], "answer": 1},
         {"q": "8. Journalists from other countries visited William's farm.",
          "options": ["True", "False", "Not Given"], "answer": 2},
         {"q": "9. William used money he received to improve water supplies in his village.",
          "options": ["True", "False", "Not Given"], "answer": 0},
         {"q": "10. The health of the villagers has improved since the windmill was built.",
          "options": ["True", "False", "Not Given"], "answer": 0},
     ]},

    # Passage 1 — short answer (Q11-13)
    {"id": "r_p3", "type": "writing", "section": "reading", "part": 3, "start_num": 11,
     "instruction": "Questions 11-13.\nAnswer the questions below.\nUse NO MORE THAN ONE WORD and/or a NUMBER from the passage for each answer.",
     "passage": "How tall was the final tower that William built? (11) ________\nWhat did the villagers use for fuel before the windmill was built? (12) ________\nWhat school subject has become more popular in William's village? (13) ________",
     "gap_items": ["39 FEET", "KEROSENE", "SCIENCE"],
     "gap_labels": ["11", "12", "13"],
     "points": 3},

    # Passage 2 — paragraph matching (Q14-18)
    {"id": "r_p4", "type": "matching", "section": "reading", "part": 4, "start_num": 14,
     "instruction": "READING PASSAGE 2. Questions 14-18.\nReading Passage 2 has eight paragraphs, A-H.\nWhich paragraph contains the following information?\nNB You may use any letter more than once.",
     "title": "White mountain, green tourism",
     "passage": CHAMONIX_TEXT,
     "points": 5,
     "options": [
         "14. a list of the type of people who enjoy going to Chamonix",
         "15. reference to a system that is changing the way visitors reach Chamonix",
         "16. the geographical location of Chamonix",
         "17. mention of the need to control the large tourist population in Chamonix",
         "18. reference to a national environmental target",
     ],
     "items": ["A", "B", "C", "D", "E", "F", "G", "H"],
     "answer": [2, 6, 0, 7, 4]},

    # Passage 2 — choose TWO (Q19-20)
    {"id": "r_p5", "type": "multiple_group", "section": "reading", "part": 5, "start_num": 19,
     "instruction": "Questions 19-20.\nChoose TWO letters, A-E.\nThe writer mentions several ways that the authorities aim to educate tourists in Chamonix. Which TWO of the following ways are mentioned?",
     "points": 2,
     "items": [
         {"q": "19. Which way is mentioned?",
          "options": ["giving instructions about litter", "imposing fines on people who drop litter", "handing out leaflets in the town", "operating a web-based information service", "having a paper-free tourist office"],
          "answer": 0},
         {"q": "20. Which other way is mentioned?",
          "options": ["giving instructions about litter", "imposing fines on people who drop litter", "handing out leaflets in the town", "operating a web-based information service", "having a paper-free tourist office"],
          "answer": 3},
     ]},

    # Passage 2 — choose TWO (Q21-22)
    {"id": "r_p6", "type": "multiple_group", "section": "reading", "part": 6, "start_num": 21,
     "instruction": "Questions 21-22.\nChoose TWO letters, A-E.\nThe writer mentions several ways that hotels are reducing their carbon emissions. Which TWO of the following ways are mentioned?",
     "points": 2,
     "items": [
         {"q": "21. Which way is mentioned?",
          "options": ["using natural cleaning materials", "recycling water", "limiting guest numbers", "providing places for rubbish", "harnessing energy from the sun"],
          "answer": 3},
         {"q": "22. Which other way is mentioned?",
          "options": ["using natural cleaning materials", "recycling water", "limiting guest numbers", "providing places for rubbish", "harnessing energy from the sun"],
          "answer": 4},
     ]},

    # Passage 2 — sentence completion (Q23-26)
    {"id": "r_p7", "type": "writing", "section": "reading", "part": 7, "start_num": 23,
     "instruction": "Questions 23-26.\nComplete the sentences below.\nChoose NO MORE THAN TWO WORDS from the passage for each answer.",
     "passage": "The first people to discover the Chamonix valley were (23) ________.\nChamonix's busiest tourist season is the (24) ________.\nPublic areas, such as the (25) ________ in Chamonix, are using fewer resources.\nThe (26) ________ on the mountains around Chamonix provide visual evidence of global warming.",
     "gap_items": ["EXPLORERS", "SUMMER", "ICE RINK", "(MELTING) GLACIERS"],
     "gap_labels": ["23", "24", "25", "26"],
     "points": 4},

    # Passage 3 — MC (Q27-31)
    {"id": "r_p8", "type": "multiple_group", "section": "reading", "part": 8, "start_num": 27,
     "instruction": "READING PASSAGE 3. Questions 27-31.\nChoose the correct letter, A, B, C or D.",
     "title": "Reading in a whole new way",
     "passage": SCREEN_TEXT,
     "points": 5,
     "items": [
         {"q": "27. What does the writer say about dictation?",
          "options": ["It helped people learn to read.", "It affected the way people wrote.", "It was not used until the 11th century.", "It was used mainly for correspondence."],
          "answer": 1},
         {"q": "28. According to the writer, what changed after the invention of the printing press?",
          "options": ["Romance became more popular than serious fiction.", "Newspapers became more popular than books.", "Readers asked for more autobiographies.", "Authors had a wider choice of topics."],
          "answer": 3},
         {"q": "29. In the third paragraph, the writer focuses on the",
          "options": ["legal concerns of authors.", "rapid changes in public libraries.", "growing status of the written word.", "recognition of the book as an art form."],
          "answer": 2},
         {"q": "30. What does the writer say about screens in the fourth paragraph?",
          "options": ["They are hard to read.", "They are bad for our health.", "They can improve our work.", "They can be found everywhere."],
          "answer": 3},
         {"q": "31. According to the writer, computers differ from television because they",
          "options": ["encourage more reading.", "attract more criticism.", "take up more of our leisure time.", "include more educational content."],
          "answer": 0},
     ]},

    # Passage 3 — Yes/No/Not Given (Q32-36)
    {"id": "r_p9", "type": "multiple_group", "section": "reading", "part": 9, "start_num": 32,
     "instruction": "Questions 32-36.\nDo the following statements agree with the views of the writer in Reading Passage 3?\nYES if the statement agrees with the views of the writer\nNO if the statement contradicts the views of the writer\nNOT GIVEN if it is impossible to say what the writer thinks about this",
     "points": 5,
     "items": [
         {"q": "32. Screen reading has reduced the number of books and newspapers people read.",
          "options": ["Yes", "No", "Not Given"], "answer": 2},
         {"q": "33. Screen literacy requires a wider range of visual skills than book-based literacy.",
          "options": ["Yes", "No", "Not Given"], "answer": 0},
         {"q": "34. Screen reading is more active than book reading.",
          "options": ["Yes", "No", "Not Given"], "answer": 0},
         {"q": "35. Screens and books produce similar thought patterns in their readers.",
          "options": ["Yes", "No", "Not Given"], "answer": 1},
         {"q": "36. People are easily persuaded to believe lies on the screen.",
          "options": ["Yes", "No", "Not Given"], "answer": 1},
     ]},

    # Passage 3 — sentence endings matching (Q37-40)
    {"id": "r_p10", "type": "matching", "section": "reading", "part": 10, "start_num": 37,
     "instruction": "Questions 37-40.\nComplete each sentence with the correct ending, A-F, below.",
     "points": 4,
     "events": [
         "the accuracy of its information.",
         "people's ability to concentrate.",
         "the global use of the Internet.",
         "how people behave physically when they read screens.",
         "the screen's ability to make an object seem real.",
         "how rapidly opinions can be communicated.",
     ],
     "options": [
         "37. The film Minority Report illustrates",
         "38. Our behaviour when we watch a film shows",
         "39. Wikipedia's success relies on",
         "40. Webkinz is an example of",
     ],
     "items": ["A", "B", "C", "D", "E", "F"],
     "answer": [3, 5, 0, 4]},
]

# ============ WRITING ============

WRITING_QUESTIONS = [
    {"id": "w1", "type": "writing", "section": "writing", "start_num": 1,
     "question": "WRITING TASK 1\nYou should spend about 20 minutes on this task.\n\nThe graph below shows the percentages of tourists who used different types of transport to travel within a particular nation between 1989 and 2009. Each tourist may have used more than one type of transport.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant.\n\nWrite at least 150 words.",
     "word_limit": "150", "points": 20},

    {"id": "w2", "type": "writing", "section": "writing", "start_num": 2,
     "question": "WRITING TASK 2\nYou should spend about 40 minutes on this task.\nWrite about the following topic:\n\nUniversity students often focus on one subject. However, some people think that universities should encourage students to learn a range of other subjects.\n\nTo what extent do you agree or disagree?\n\nGive reasons for your answer and include any relevant examples from your own knowledge and experience.\n\nWrite at least 250 words.",
     "word_limit": "250", "points": 20},
]

questions = LISTENING_QUESTIONS + READING_QUESTIONS + WRITING_QUESTIONS

test = {
    "section": "novice_end",
    "title": "🌱 NOVICE · END",
    "icon": "🌱",
    "time_limit": 55,
    "price": 0,
    "original_price": 0,
    "active": True,
    "description": "Novice daraja yakuniy imtihoni — Listening + Reading + Writing",
    "audio_parts": [AUDIO, AUDIO, AUDIO, AUDIO],
    "created_at": datetime.now(timezone.utc),
    "questions": questions,
}


def seed_novice_end(db):
    """Insert or update the NOVICE END test document (keeps _id stable so old attempts work)."""
    db.tests.update_one(
        {"section": "novice_end"},
        {"$set": test},
        upsert=True,
    )
    return len(test["questions"])
