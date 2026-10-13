import re
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Agentic Dating Site", version="1.0.0")
templates = Jinja2Templates(directory="templates")

# User-supplied public profile summaries with generated dating analysis.
PROFILES: list[dict[str, Any]] = [
    {"id": 1, "name": "Sam Altman", "title": "CEO, OpenAI", "linkedin": "https://www.linkedin.com/in/samaltman", "instagram": "https://www.instagram.com/samaltman", "hobbies": ["AI Safety", "Angel Investing", "Racing Cars", "Hiking"], "needs": "Looking for an intellectually curious partner who enjoys long philosophical walks and thinking about the future.", "bio": "Entrepreneur, investor, and tech builder focused on scaling transformative technologies and AGI."},
    {"id": 2, "name": "Satya Nadella", "title": "CEO, Microsoft", "linkedin": "https://www.linkedin.com/in/satyanadella", "instagram": "https://www.instagram.com/satyanadella", "hobbies": ["Cricket", "Poetry", "Empathetic Leadership", "Reading"], "needs": "Seeking someone grounded who values empathy, continuous learning, and peaceful weekend tea sessions.", "bio": "Transformational tech executive passionate about culture change, growth mindsets, and global impact."},
    {"id": 3, "name": "Marques Brownlee (MKBHD)", "title": "Tech Creator & Ultimate Frisbee Athlete", "linkedin": "https://www.linkedin.com/in/marquesbrownlee", "instagram": "https://www.instagram.com/mkbhd", "hobbies": ["Ultimate Frisbee", "Consumer Tech", "Video Production", "Electric Vehicles"], "needs": "Looking for a high-energy partner who loves active outdoor sports, crisp visuals, and tech innovations.", "bio": "Tech reviewer, podcast co-host, and semi-pro Ultimate Frisbee player focused on quality and design."},
    {"id": 4, "name": "Jimmy Donaldson (MrBeast)", "title": "Founder, Beast Industries", "linkedin": "https://www.linkedin.com/in/jimmy-donaldson-mrbeast", "instagram": "https://www.instagram.com/mrbeast", "hobbies": ["Philanthropy", "Viral Stunts", "Chocolate Making", "Basketball"], "needs": "Seeking someone adventurous, patient, and driven by giving back to the community on a massive scale.", "bio": "Digital creator and philanthropist passionate about setting global records and scaling consumer brands."},
    {"id": 5, "name": "Lex Fridman", "title": "AI Research Scientist & Podcaster", "linkedin": "https://www.linkedin.com/in/lexfridman", "instagram": "https://www.instagram.com/lexfridman", "hobbies": ["Jiu-Jitsu", "Acoustic Guitar", "Deep Conversations", "Robotics"], "needs": "Searching for deep emotional connection, mutual respect, love, and long late-night talks about science and heart.", "bio": "Research scientist in autonomous systems and host of deep-form conversations exploring humanity."},
    {"id": 6, "name": "Serena Williams", "title": "Founder, Serena Ventures", "linkedin": "https://www.linkedin.com/in/serenawilliams", "instagram": "https://www.instagram.com/serenawilliams", "hobbies": ["Tennis", "Fashion Design", "Venture Capital", "Fitness"], "needs": "Looking for a confident, supportive partner who appreciates athletics, high style, and entrepreneurial grit.", "bio": "Tennis icon, fashion designer, and investor helping diverse founders build category-defining ventures."},
    {"id": 7, "name": "Andrew Ng", "title": "Founder, DeepLearning.AI & AI Fund", "linkedin": "https://www.linkedin.com/in/andrewng", "instagram": "https://www.instagram.com/andrewng", "hobbies": ["Machine Learning", "Teaching", "Coding", "Tea Tasting"], "needs": "Seeking a thoughtful partner who loves learning new concepts, education, and calm intellectual exchanges.", "bio": "Pioneer in artificial intelligence education, online learning platforms, and venture incubation."},
    {"id": 8, "name": "Sara Blakely", "title": "Founder, Spanx & Investor", "linkedin": "https://www.linkedin.com/in/sarablakely", "instagram": "https://www.instagram.com/sarablakely", "hobbies": ["Entrepreneurship", "Public Speaking", "Creative Humor", "Family Time"], "needs": "Looking for a fun, uplifting partner who isn't afraid to laugh at themselves and embrace spontaneous ideas.", "bio": "Self-made entrepreneur, inventor, and philanthropist dedicated to supporting female-led businesses."},
    {"id": 9, "name": "Alex Hormozi", "title": "Co-founder, Acquisition.com", "linkedin": "https://www.linkedin.com/in/alexhormozi", "instagram": "https://www.instagram.com/hormozi", "hobbies": ["Weightlifting", "Business Strategy", "Content Creation", "Book Writing"], "needs": "Seeking an ambitious, disciplined, and straight-shooting partner focused on self-mastery and long-term goals.", "bio": "Investor, author, and entrepreneur building high-growth business portfolios and educational content."},
    {"id": 10, "name": "Gwyneth Paltrow", "title": "Founder & CEO, Goop", "linkedin": "https://www.linkedin.com/in/gwynethpaltrow", "instagram": "https://www.instagram.com/gwynethpaltrow", "hobbies": ["Wellness", "Organic Cooking", "Skincare", "Interior Design"], "needs": "Looking for an intentional, conscious partner who values holistic living, quiet luxury, and culinary arts.", "bio": "Academy Award-winning actor turned lifestyle entrepreneur building wellness and beauty platforms."},
    {"id": 11, "name": "Brian Chesky", "title": "Co-founder & CEO, Airbnb", "linkedin": "https://www.linkedin.com/in/brianchesky", "instagram": "https://www.instagram.com/brianchesky", "hobbies": ["Industrial Design", "Travel", "Bodybuilding", "Architecture"], "needs": "Seeking a creative wanderer who loves immaculate design, world cultures, and host hospitality.", "bio": "Designer and tech executive passionate about reshaping how people experience space and community."},
    {"id": 12, "name": "Fei-Fei Li", "title": "Co-Director, Stanford Human-Centered AI", "linkedin": "https://www.linkedin.com/in/fei-fei-li-stanford", "instagram": None, "hobbies": ["Computer Vision", "Ethics in Tech", "Mentorship", "Museums"], "needs": "Looking for a grounded thinker who believes in human-first technology and thoughtful storytelling.", "bio": "AI researcher, professor, and author leading human-centered artificial intelligence initiatives."},
    {"id": 13, "name": "Mark Cuban", "title": "Co-founder, Cost Plus Drugs", "linkedin": "https://www.linkedin.com/in/mark-cuban-bb386", "instagram": "https://www.instagram.com/mcuban", "hobbies": ["Healthcare Reform", "Basketball", "Startups", "Reading Pitch Decks"], "needs": "Seeking a sharp, energetic companion who loves lively debates, court-side games, and disrupting monopolies.", "bio": "Investor, entrepreneur, and owner focused on transparent pricing and venture backing."},
    {"id": 14, "name": "Reshma Saujani", "title": "Founder, Girls Who Code & Moms First", "linkedin": "https://www.linkedin.com/in/reshmasaujani", "instagram": "https://www.instagram.com/reshmasaujani", "hobbies": ["Gender Equity", "Public Policy", "Writing", "Community Organizing"], "needs": "Looking for a passionate partner who stands for bravery over perfection and values equality.", "bio": "Author and advocate building movement initiatives to close the gender gap in tech and workforce policy."},
    {"id": 15, "name": "Jay Shetty", "title": "Author & Host, On Purpose", "linkedin": "https://www.linkedin.com/in/jayshetty", "instagram": "https://www.instagram.com/jayshetty", "hobbies": ["Meditation", "Mindfulness", "Storytelling", "Plant-based Food"], "needs": "Seeking a spiritual, emotionally open soul who prioritizes mental wellbeing and intentional listening.", "bio": "Former monk turned author and podcast host sharing wisdom and purpose-driven daily practices."},
    {"id": 16, "name": "Alexis Ohanian", "title": "Founder, Seven Seven Six & Co-founder, Reddit", "linkedin": "https://www.linkedin.com/in/alexisohanian", "instagram": "https://www.instagram.com/alexisohanian", "hobbies": ["Women's Sports", "Pancake Art", "Venture Investing", "Gaming"], "needs": "Seeking a witty, creative partner who loves internet culture, sports elevation, and family rituals.", "bio": "Venture capitalist and entrepreneur passionate about championing women's athletics and tech startups."},
    {"id": 17, "name": "Arianna Huffington", "title": "Founder & CEO, Thrive Global", "linkedin": "https://www.linkedin.com/in/ariannahuffington", "instagram": "https://www.instagram.com/ariannahuff", "hobbies": ["Sleep Hygiene", "Wellbeing", "Classical Literature", "Walks in Nature"], "needs": "Looking for someone who respects healthy boundaries, avoids burnout, and appreciates deep conversations.", "bio": "Media pioneer and author building behavior-change platforms to improve human health and performance."},
    {"id": 18, "name": "Casey Neistat", "title": "Filmmaker & YouTube Creator", "linkedin": "https://www.linkedin.com/in/caseyneistat", "instagram": "https://www.instagram.com/caseyneistat", "hobbies": ["Marathon Running", "Filmmaking", "DIY Engineering", "NYC Skateboarding"], "needs": "Seeking a gritty, unconventional partner who thrives on relentless momentum and storytelling.", "bio": "New York City filmmaker and visual storyteller known for pushing creative production boundaries."},
    {"id": 19, "name": "Tim Ferriss", "title": "Author & Host, The Tim Ferriss Show", "linkedin": "https://www.linkedin.com/in/timferriss", "instagram": "https://www.instagram.com/timferriss", "hobbies": ["Biohacking", "Cold Plunges", "Language Learning", "Dog Training"], "needs": "Looking for an analytical yet curious mind who loves experimenting with life hacks and quiet solitude.", "bio": "Author and early-stage investor exploring high performance, mental health, and rapid skill acquisition."},
    {"id": 20, "name": "Dr. Andrew Huberman", "title": "Professor of Neurobiology, Stanford Medicine", "linkedin": "https://www.linkedin.com/in/andrew-huberman", "instagram": "https://www.instagram.com/hubermanlab", "hobbies": ["Morning Sunlight", "Neuroscience", "Weight Training", "Skateboarding"], "needs": "Seeking a routine-oriented partner who appreciates health science, discipline, and nature hikes.", "bio": "Neuroscientist and host of the Huberman Lab podcast sharing protocol-based science for daily life."},
    {"id": 21, "name": "Steven Bartlett", "title": "Host, The Diary Of A CEO & Investor", "linkedin": "https://www.linkedin.com/in/stevenbartlett-123", "instagram": "https://www.instagram.com/steven", "hobbies": ["Podcasting", "Health Tech", "Public Speaking", "Music Production"], "needs": "Looking for an authentic, self-aware partner who values honest communication and personal growth.", "bio": "Entrepreneur, speaker, and investor examining modern leadership, psychology, and wellness."},
    {"id": 22, "name": "Shonda Rhimes", "title": "CEO, Shondaland", "linkedin": "https://www.linkedin.com/in/shondarhimes", "instagram": "https://www.instagram.com/shondarhimes", "hobbies": ["Screenwriting", "Story Development", "Gourmet Coffee", "Gardening"], "needs": "Seeking a partner with emotional depth, a strong work ethic, and a love for captivating drama.", "bio": "Television producer, screenwriter, and author building iconic narrative franchises and production teams."},
    {"id": 23, "name": "Iman Gadzhi", "title": "Founder, Educate.io", "linkedin": "https://www.linkedin.com/in/iman-gadzhi", "instagram": "https://www.instagram.com/gadzhi", "hobbies": ["Fine Watches", "Self-Education", "Fitness", "Digital Media"], "needs": "Seeking an ambitious companion who appreciates high aesthetics, discipline, and continuous evolution.", "bio": "Digital entrepreneur and content creator focused on online skills education and agency building."},
    {"id": 24, "name": "Mel Robbins", "title": "Host, The Mel Robbins Podcast & Author", "linkedin": "https://www.linkedin.com/in/melrobbins", "instagram": "https://www.instagram.com/melrobbins", "hobbies": ["Motivation", "Journaling", "Dog Walking", "Relationship Coaching"], "needs": "Looking for a warm, transparent partner who takes action, practices encouragement, and values honesty.", "bio": "Author and speaker teaching research-backed tools for confidence, mindset shifts, and habit building."},
    {"id": 25, "name": "Guy Raz", "title": "Host & Co-creator, How I Built This", "linkedin": "https://www.linkedin.com/in/guy-raz-a1288b13", "instagram": "https://www.instagram.com/guy.raz", "hobbies": ["Journalism", "Audio Storytelling", "Acoustic Music", "Cycling"], "needs": "Seeking a curious, empathetic storyteller who loves exploring how things work and learning from resilience.", "bio": "Broadcaster and author interviewing world-class founders to uncover journey insights and startup lessons."},
]

INTEREST_RULES = {
    "Technology": ("ai", "tech", "technology", "coding", "robotics", "computer vision", "machine learning", "digital media", "artificial intelligence", "electric vehicles"),
    "Business & investing": ("investor", "investing", "venture", "business", "startup", "founder", "entrepreneur", "agency", "capital", "pitch", "scaling", "acquisition"),
    "Sports & fitness": ("sports", "tennis", "fitness", "weightlifting", "basketball", "running", "jiu-jitsu", "skateboarding", "athlete", "training", "hiking", "racing cars", "cricket", "bodybuilding"),
    "Media & storytelling": ("podcast", "story", "journalism", "filmmaking", "film", "writing", "screenwriting", "video production", "content creation", "broadcast", "host", "media", "creator", "public speaking", "audio"),
    "Arts & design": ("design", "art", "poetry", "guitar", "music", "fashion", "architecture", "creative", "museum", "piano", "drama", "literature", "photography"),
    "Health & wellness": ("wellness", "health", "meditation", "mindfulness", "sleep", "mental health", "biohacking", "cold plunges", "neuroscience", "relationship coaching", "skincare", "yoga", "wellbeing"),
    "Education & research": ("teaching", "education", "learning", "research", "scientist", "professor", "mentorship", "author", "reading", "self-education"),
    "Community & impact": ("philanthropy", "community", "equity", "public policy", "advocate", "gender", "impact", "reform", "mentorship"),
    "Food & hospitality": ("cooking", "food", "chocolate", "culinary", "coffee", "tea", "hospitality", "pancake"),
    "Travel & culture": ("travel", "culture", "language", "world cultures", "walks in nature"),
}

TRAIT_RULES = {
    "Curious": ("curious", "learning", "research", "science", "exploring", "experiments", "questions"),
    "Creative": ("creative", "design", "writing", "storytelling", "filmmaking", "art", "inventor"),
    "Goal-oriented": ("entrepreneur", "founder", "investor", "scaling", "building", "ambitious", "disciplined"),
    "Community-minded": ("community", "philanthropist", "advocate", "equity", "mentorship", "supporting"),
    "Active": ("sports", "tennis", "running", "fitness", "hiking", "cycling", "athlete", "training"),
    "Reflective": ("poetry", "mindfulness", "meditation", "philosophical", "mental health", "literature"),
    "People-focused": ("teaching", "empathy", "empathetic", "mentor", "human-centered", "relationships"),
}


def derive_tags(profile: dict[str, Any], rules: dict[str, tuple[str, ...]]) -> list[str]:
    text = " ".join([profile["title"], profile["bio"], *profile["hobbies"]]).casefold()
    return [
        label
        for label, phrases in rules.items()
        if any(re.search(rf"\b{re.escape(phrase)}\b", text) for phrase in phrases)
    ]


for profile in PROFILES:
    profile["interests"] = derive_tags(profile, INTEREST_RULES)
    profile["traits"] = derive_tags(profile, TRAIT_RULES)


PROFILE_BY_ID = {profile["id"]: profile for profile in PROFILES}


def compatibility(first: dict[str, Any], second: dict[str, Any]) -> int:
    shared_interests = len(set(first["interests"]) & set(second["interests"]))
    shared_traits = len(set(first["traits"]) & set(second["traits"]))
    shared_hobbies = len({hobby.casefold() for hobby in first["hobbies"]} & {hobby.casefold() for hobby in second["hobbies"]})
    return min(97, 48 + shared_interests * 8 + shared_traits * 3 + shared_hobbies * 10)


def ranked_matches(profile: dict[str, Any], limit: int = 3) -> list[dict[str, Any]]:
    matches = [candidate for candidate in PROFILES if candidate["id"] != profile["id"]]
    matches.sort(key=lambda candidate: (-compatibility(profile, candidate), candidate["id"]))
    return [
        {"id": candidate["id"], "name": candidate["name"], "title": candidate["title"], "compatibility": compatibility(profile, candidate)}
        for candidate in matches[:limit]
    ]


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request, "profiles": PROFILES})


@app.get("/api/simulate-date/{id1}/{id2}")
def simulate_date(id1: int, id2: int) -> dict[str, Any]:
    first = PROFILE_BY_ID.get(id1)
    second = PROFILE_BY_ID.get(id2)
    if first is None or second is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    if id1 == id2:
        raise HTTPException(status_code=400, detail="Choose two different profiles")

    shared = sorted(set(first["interests"]) & set(second["interests"]))
    shared_topic = shared[0] if shared else "an interest they could explore together"
    second_need = re.sub(r"^(looking for|seeking|searching for)\s+", "", second["needs"], flags=re.IGNORECASE).rstrip(".")
    messages = [
        {"speaker": f"Agent for {first['name']}", "message": f"The supplied scenario notes that {second['name']} is interested in {second_need}. What is an easy way for the two profiles to start a conversation?"},
        {"speaker": f"Agent for {second['name']}", "message": f"Their profile summaries share themes around {shared_topic}. A relaxed conversation about that could be a good starting point."},
        {"speaker": f"Agent for {first['name']}", "message": f"{first['name']}'s listed hobbies include {first['hobbies'][0].lower()}. We could also ask {second['name']} about {second['hobbies'][0].lower()}."},
        {"speaker": f"Agent for {second['name']}", "message": "That sounds like a thoughtful introduction. The profiles can compare interests and see where the conversation goes."},
    ]
    return {"person1": first["name"], "person2": second["name"], "compatibility": compatibility(first, second), "messages": messages}


@app.get("/api/rankings")
def rankings() -> dict[str, Any]:
    return {
        "rankings": [
            {"person": {"id": profile["id"], "name": profile["name"]}, "matches": ranked_matches(profile)}
            for profile in PROFILES
        ]
    }
