"""
30 Questions for IT Career Prediction
Categorized into 6 groups of 5 questions each:
1. Personality & Work Style
2. Problem Solving & Thinking
3. Interests & Passions
4. Social & Communication
5. Technical Exposure & Qualifications
6. Goals & Environment
"""

QUESTIONS = [
    # ─── CATEGORY 1: Personality & Work Style ───────────────────────────────
    {
        "id": 1,
        "category": "Personality & Work Style",
        "category_icon": "🧠",
        "text": "When you face a new task you've never done before, what do you usually do first?",
        "options": [
            {"value": "a", "label": "Jump in and figure it out as I go"},
            {"value": "b", "label": "Read guides or watch tutorials before starting"},
            {"value": "c", "label": "Ask someone experienced for advice"},
            {"value": "d", "label": "Break it into small steps and plan carefully"},
        ]
    },
    {
        "id": 2,
        "category": "Personality & Work Style",
        "category_icon": "🧠",
        "text": "How do you feel after working on the same task for 3-4 hours straight?",
        "options": [
            {"value": "a", "label": "Energized — I can keep going"},
            {"value": "b", "label": "Fine, but I need a short break"},
            {"value": "c", "label": "Tired — I prefer switching tasks frequently"},
            {"value": "d", "label": "It depends on how interesting the task is"},
        ]
    },
    {
        "id": 3,
        "category": "Personality & Work Style",
        "category_icon": "🧠",
        "text": "How do you feel when your work is being reviewed or criticized?",
        "options": [
            {"value": "a", "label": "I welcome it — feedback helps me grow"},
            {"value": "b", "label": "I'm okay with it but it takes time to process"},
            {"value": "c", "label": "I feel uncomfortable but I manage"},
            {"value": "d", "label": "I prefer to self-review before sharing"},
        ]
    },
    {
        "id": 4,
        "category": "Personality & Work Style",
        "category_icon": "🧠",
        "text": "You have a week to complete a project. How do you usually work?",
        "options": [
            {"value": "a", "label": "Finish it in the first 2 days"},
            {"value": "b", "label": "Spread it evenly across the week"},
            {"value": "c", "label": "Work mostly in the last 2-3 days under pressure"},
            {"value": "d", "label": "Work in intense bursts whenever I feel motivated"},
        ]
    },
    {
        "id": 5,
        "category": "Personality & Work Style",
        "category_icon": "🧠",
        "text": "Which best describes how you like to work?",
        "options": [
            {"value": "a", "label": "Alone, fully focused with no interruptions"},
            {"value": "b", "label": "In a small team of 2-3 trusted people"},
            {"value": "c", "label": "In a big, buzzing team with lots of collaboration"},
            {"value": "d", "label": "It varies — I enjoy both solo and team work"},
        ]
    },

    # ─── CATEGORY 2: Problem Solving & Thinking ─────────────────────────────
    {
        "id": 6,
        "category": "Problem Solving & Thinking",
        "category_icon": "🔍",
        "text": "When something breaks (like your phone, app, or gadget), what do you do?",
        "options": [
            {"value": "a", "label": "Try to fix it myself before asking for help"},
            {"value": "b", "label": "Search online for a solution"},
            {"value": "c", "label": "Hand it to someone who knows better"},
            {"value": "d", "label": "Observe the problem carefully before doing anything"},
        ]
    },
    {
        "id": 7,
        "category": "Problem Solving & Thinking",
        "category_icon": "🔍",
        "text": "Which activity would you find most satisfying?",
        "options": [
            {"value": "a", "label": "Finding a hidden bug in code that no one else could find"},
            {"value": "b", "label": "Designing a beautiful user interface from scratch"},
            {"value": "c", "label": "Analyzing a large dataset to find patterns"},
            {"value": "d", "label": "Building a system that handles thousands of users"},
        ]
    },
    {
        "id": 8,
        "category": "Problem Solving & Thinking",
        "category_icon": "🔍",
        "text": "How do you typically approach a complex problem?",
        "options": [
            {"value": "a", "label": "Visualize it — draw diagrams or mind maps"},
            {"value": "b", "label": "Break it into sub-problems logically"},
            {"value": "c", "label": "Look for similar solved problems as reference"},
            {"value": "d", "label": "Discuss it with others to get multiple angles"},
        ]
    },
    {
        "id": 9,
        "category": "Problem Solving & Thinking",
        "category_icon": "🔍",
        "text": "You discover two solutions to a problem — one fast but risky, one slow but safe. You choose:",
        "options": [
            {"value": "a", "label": "Fast and risky — I'll deal with issues if they arise"},
            {"value": "b", "label": "Safe and slow — reliability matters more"},
            {"value": "c", "label": "Try the fast one first, with a backup plan"},
            {"value": "d", "label": "Analyze both thoroughly before deciding"},
        ]
    },
    {
        "id": 10,
        "category": "Problem Solving & Thinking",
        "category_icon": "🔍",
        "text": "Which of these school/college subjects did you enjoy the most?",
        "options": [
            {"value": "a", "label": "Mathematics or Logic"},
            {"value": "b", "label": "Art, Design, or Graphics"},
            {"value": "c", "label": "Science or Computer Studies"},
            {"value": "d", "label": "Communication, English, or Social Studies"},
        ]
    },

    # ─── CATEGORY 3: Interests & Passions ───────────────────────────────────
    {
        "id": 11,
        "category": "Interests & Passions",
        "category_icon": "❤️",
        "text": "In your free time, which of these activities appeals to you most?",
        "options": [
            {"value": "a", "label": "Playing or tinkering with gadgets and software"},
            {"value": "b", "label": "Drawing, designing, or creating digital art"},
            {"value": "c", "label": "Reading about tech news, AI, or science"},
            {"value": "d", "label": "Helping others solve problems or teaching"},
        ]
    },
    {
        "id": 12,
        "category": "Interests & Passions",
        "category_icon": "❤️",
        "text": "If you could build anything, what would excite you most?",
        "options": [
            {"value": "a", "label": "A mobile app that solves a daily problem"},
            {"value": "b", "label": "A game or interactive experience"},
            {"value": "c", "label": "An AI model that predicts something useful"},
            {"value": "d", "label": "A secure system to protect people's data"},
        ]
    },
    {
        "id": 13,
        "category": "Interests & Passions",
        "category_icon": "❤️",
        "text": "Which tech topic do you find yourself reading or watching videos about?",
        "options": [
            {"value": "a", "label": "Hacking, cybersecurity, and online safety"},
            {"value": "b", "label": "AI, machine learning, and chatbots"},
            {"value": "c", "label": "Web or app development"},
            {"value": "d", "label": "Cloud computing, servers, and infrastructure"},
        ]
    },
    {
        "id": 14,
        "category": "Interests & Passions",
        "category_icon": "❤️",
        "text": "When using an app or website, what do you notice first?",
        "options": [
            {"value": "a", "label": "How it looks and how easy it is to use"},
            {"value": "b", "label": "Whether it's fast and doesn't crash"},
            {"value": "c", "label": "Whether it feels secure and trustworthy"},
            {"value": "d", "label": "The features it offers and what it can do"},
        ]
    },
    {
        "id": 15,
        "category": "Interests & Passions",
        "category_icon": "❤️",
        "text": "Which real-world problem would you most want to solve using technology?",
        "options": [
            {"value": "a", "label": "Making education accessible to rural areas"},
            {"value": "b", "label": "Detecting fraud and protecting people online"},
            {"value": "c", "label": "Using data to improve healthcare outcomes"},
            {"value": "d", "label": "Automating boring tasks so people have more time"},
        ]
    },

    # ─── CATEGORY 4: Social & Communication ─────────────────────────────────
    {
        "id": 16,
        "category": "Social & Communication",
        "category_icon": "💬",
        "text": "How comfortable are you speaking in front of a group of people?",
        "options": [
            {"value": "a", "label": "Very comfortable — I enjoy presenting"},
            {"value": "b", "label": "Okay with it, but I prepare a lot beforehand"},
            {"value": "c", "label": "Nervous but I manage when I have to"},
            {"value": "d", "label": "I strongly prefer written communication"},
        ]
    },
    {
        "id": 17,
        "category": "Social & Communication",
        "category_icon": "💬",
        "text": "In a group project, which role do you usually take?",
        "options": [
            {"value": "a", "label": "Leader — I plan and coordinate the team"},
            {"value": "b", "label": "Doer — I focus on executing the tasks well"},
            {"value": "c", "label": "Creative — I come up with ideas and designs"},
            {"value": "d", "label": "Analyzer — I review work and spot issues"},
        ]
    },
    {
        "id": 18,
        "category": "Social & Communication",
        "category_icon": "💬",
        "text": "How do you explain something complicated to a friend who knows nothing about it?",
        "options": [
            {"value": "a", "label": "Use simple analogies and real-life examples"},
            {"value": "b", "label": "Show them step by step with demos"},
            {"value": "c", "label": "Draw it out or use diagrams"},
            {"value": "d", "label": "I find it hard — I prefer technical discussions"},
        ]
    },
    {
        "id": 19,
        "category": "Social & Communication",
        "category_icon": "💬",
        "text": "When working with clients or users, what matters most to you?",
        "options": [
            {"value": "a", "label": "Understanding exactly what they need"},
            {"value": "b", "label": "Delivering something that works perfectly"},
            {"value": "c", "label": "Making sure they're happy with the experience"},
            {"value": "d", "label": "Explaining technical decisions clearly"},
        ]
    },
    {
        "id": 20,
        "category": "Social & Communication",
        "category_icon": "💬",
        "text": "Which of these sounds like your ideal work scenario?",
        "options": [
            {"value": "a", "label": "Leading strategy meetings and guiding a team"},
            {"value": "b", "label": "Writing clean code or building systems alone"},
            {"value": "c", "label": "Brainstorming creative solutions with designers"},
            {"value": "d", "label": "Researching and analyzing data independently"},
        ]
    },

    # ─── CATEGORY 5: Technical Exposure & Qualifications ────────────────────
    {
        "id": 21,
        "category": "Technical Exposure & Qualifications",
        "category_icon": "🎓",
        "text": "What is your current level of education or study?",
        "options": [
            {"value": "a", "label": "Still in school (10th/12th grade)"},
            {"value": "b", "label": "College student (any stream)"},
            {"value": "c", "label": "Graduate or post-graduate"},
            {"value": "d", "label": "Already working / self-taught"},
        ]
    },
    {
        "id": 22,
        "category": "Technical Exposure & Qualifications",
        "category_icon": "🎓",
        "text": "Have you ever tried any of the following? (Pick the highest level you've reached)",
        "options": [
            {"value": "a", "label": "Never tried any coding or technical activity"},
            {"value": "b", "label": "Tried online tutorials or short courses"},
            {"value": "c", "label": "Built a small project (website, app, etc.)"},
            {"value": "d", "label": "Worked on real projects or professional work"},
        ]
    },
    {
        "id": 23,
        "category": "Technical Exposure & Qualifications",
        "category_icon": "🎓",
        "text": "How confident are you with computers and technology in daily life?",
        "options": [
            {"value": "a", "label": "Basic — I use apps but don't go deeper"},
            {"value": "b", "label": "Moderate — I install software and troubleshoot"},
            {"value": "c", "label": "Good — I customize settings and know shortcuts"},
            {"value": "d", "label": "Advanced — I configure systems and networks"},
        ]
    },
    {
        "id": 24,
        "category": "Technical Exposure & Qualifications",
        "category_icon": "🎓",
        "text": "Which of the following have you heard of or used before?",
        "options": [
            {"value": "a", "label": "None of these — I'm new to IT concepts"},
            {"value": "b", "label": "HTML/CSS or basic coding concepts"},
            {"value": "c", "label": "Python, JavaScript, or any programming language"},
            {"value": "d", "label": "Databases, APIs, cloud platforms, or networking"},
        ]
    },
    {
        "id": 25,
        "category": "Technical Exposure & Qualifications",
        "category_icon": "🎓",
        "text": "What best describes your background or field of study?",
        "options": [
            {"value": "a", "label": "Arts, Commerce, or Humanities"},
            {"value": "b", "label": "Science (PCM/PCB) without computers"},
            {"value": "c", "label": "Computer Science or IT related"},
            {"value": "d", "label": "Engineering or other technical fields"},
        ]
    },

    # ─── CATEGORY 6: Goals & Work Environment ───────────────────────────────
    {
        "id": 26,
        "category": "Goals & Work Environment",
        "category_icon": "🎯",
        "text": "What is your main goal in choosing an IT career?",
        "options": [
            {"value": "a", "label": "High salary and financial stability"},
            {"value": "b", "label": "Work I find genuinely interesting and engaging"},
            {"value": "c", "label": "Making a social impact through technology"},
            {"value": "d", "label": "Flexibility — remote work and freedom"},
        ]
    },
    {
        "id": 27,
        "category": "Goals & Work Environment",
        "category_icon": "🎯",
        "text": "Which work environment would you thrive in most?",
        "options": [
            {"value": "a", "label": "A fast-paced startup with varied tasks"},
            {"value": "b", "label": "A structured corporate tech company"},
            {"value": "c", "label": "Freelancing from home on my own schedule"},
            {"value": "d", "label": "A research lab or academic environment"},
        ]
    },
    {
        "id": 28,
        "category": "Goals & Work Environment",
        "category_icon": "🎯",
        "text": "How do you feel about continuous learning in your career?",
        "options": [
            {"value": "a", "label": "I love it — tech evolves and so should I"},
            {"value": "b", "label": "It's necessary, so I'll do what it takes"},
            {"value": "c", "label": "I'd prefer a stable skill set I can master deeply"},
            {"value": "d", "label": "I'm still figuring out what I enjoy learning"},
        ]
    },
    {
        "id": 29,
        "category": "Goals & Work Environment",
        "category_icon": "🎯",
        "text": "Where do you see yourself in 5 years?",
        "options": [
            {"value": "a", "label": "Leading a team or managing a product"},
            {"value": "b", "label": "Being a deep technical expert in one area"},
            {"value": "c", "label": "Running my own tech startup or consultancy"},
            {"value": "d", "label": "Still exploring and discovering what fits me"},
        ]
    },
    {
        "id": 30,
        "category": "Goals & Work Environment",
        "category_icon": "🎯",
        "text": "If IT turns out not to be a good fit for you, what would you do?",
        "options": [
            {"value": "a", "label": "I'm confident IT is right for me"},
            {"value": "b", "label": "Explore IT-adjacent roles like tech sales or support"},
            {"value": "c", "label": "Use tech as a tool in another career (e.g. business, health)"},
            {"value": "d", "label": "I'm open to any direction — I'm still exploring"},
        ]
    },
]

CATEGORIES = [
    {"name": "Personality & Work Style", "icon": "🧠", "questions": [1, 2, 3, 4, 5]},
    {"name": "Problem Solving & Thinking", "icon": "🔍", "questions": [6, 7, 8, 9, 10]},
    {"name": "Interests & Passions", "icon": "❤️", "questions": [11, 12, 13, 14, 15]},
    {"name": "Social & Communication", "icon": "💬", "questions": [16, 17, 18, 19, 20]},
    {"name": "Technical Exposure & Qualifications", "icon": "🎓", "questions": [21, 22, 23, 24, 25]},
    {"name": "Goals & Work Environment", "icon": "🎯", "questions": [26, 27, 28, 29, 30]},
]

TOTAL_QUESTIONS = len(QUESTIONS)
