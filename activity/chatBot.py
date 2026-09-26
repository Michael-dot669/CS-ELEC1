import random
import re

HERO_BUILDS = {
    "aldous": ["Endless Battle", "Blade of Despair", "Berserker's Fury", "Brute Force Breastplate", "Immortality", "Warrior Boots"],
    "miya": ["Berserker's Fury", "Windtalker", "Malefic Roar", "Blade of Despair", "Wind of Nature", "Swift Boots"],
    "chou": ["Endless Battle", "Blade of Despair", "Berserker's Fury", "Brute Force Breastplate", "Immortality", "Warrior Boots"],
    "alucard": ["Endless Battle", "Blade of Despair", "Berserker's Fury", "Haas's Claws", "Immortality", "Warrior Boots"],
    "eudora": ["Genius Wand", "Lightning Truncheon", "Holy Crystal", "Clock of Destiny", "Divine Glaive", "Arcane Boots"],
    "gusion": ["Genius Wand", "Lightning Truncheon", "Holy Crystal", "Concentrated Energy", "Divine Glaive", "Swift Boots"],
    "ling": ["Berserker's Fury", "Malefic Roar", "Blade of Despair", "Endless Battle", "Wind of Nature", "Swift Boots"],
    "fanny": ["Berserker's Fury", "Malefic Roar", "Blade of Despair", "Endless Battle", "Windtalker", "Swift Boots"],
    "tigreal": ["Athena's Shield", "Antique Cuirass", "Dominance Ice", "Immortality", "Oracle", "Tough Boots"],
    "grock": ["Athena's Shield", "Antique Cuirass", "Dominance Ice", "Immortality", "Radiant Armor", "Tough Boots"],
    "clint": ["Berserker's Fury", "Malefic Roar", "Windtalker", "Blade of Despair", "Wind of Nature", "Swift Boots"],
    "novaria": ["Genius Wand", "Lightning Truncheon", "Holy Crystal", "Concentrated Energy", "Divine Glaive", "Arcane Boots"],
    "lapu lapu": ["Endless Battle", "Blade of Despair", "Berserker's Fury", "Brute Force Breastplate", "Immortality", "Warrior Boots"],
    "aurora": ["Genius Wand", "Ice Queen Wand", "Holy Crystal", "Clock of Destiny", "Divine Glaive", "Arcane Boots"],
}

HERO_ROLES = {
    "aldous": "Fighter",
    "miya": "Marksman",
    "chou": "Fighter",
    "alucard": "Fighter",
    "eudora": "Mage",
    "gusion": "Assassin",
    "ling": "Assassin",
    "fanny": "Assassin",
    "tigreal": "Tank",
    "grock": "Tank",
    "clint": "Marksman",
    "novaria": "Mage",
    "lapu lapu": "Fighter",
    "aurora": "Mage",
}

HERO_DISPLAY = {
    "lapu lapu": "Lapu-Lapu",
}

HERO_EMBLEM = {
    "aldous": "Fighter Emblem - prioritize the Bravery talent for bonus Physical Attack when your HP is low.",
    "miya": "Marksman Emblem - prioritize Weakness Finder for bonus damage against low-HP enemies.",
    "chou": "Fighter Emblem - prioritize Festival of Blood for lifesteal while using Fighter Mastery.",
    "alucard": "Fighter Emblem - prioritize Festival of Blood, fits his sustain playstyle.",
    "eudora": "Mage Emblem - prioritize Impure Rage for bonus burst damage on your first skill.",
    "gusion": "Assassin Emblem - prioritize Agility for faster cooldown reduction.",
    "ling": "Assassin Emblem - prioritize Agility to match his fast combo speed.",
    "fanny": "Assassin Emblem - prioritize Agility for faster Cable movement and burst.",
    "tigreal": "Tank/Support Emblem - prioritize Vein Ripper or Brave Smite depending on your engage style.",
    "grock": "Tank Emblem - prioritize Brave Smite for extra tankiness while engaging.",
    "clint": "Marksman Emblem - prioritize Weakness Finder, standard for marksmen.",
    "novaria": "Mage Emblem - prioritize Impure Rage for her burst combo.",
    "lapu lapu": "Fighter Emblem - prioritize Bravery to match his stance-switching playstyle.",
    "aurora": "Mage Emblem - prioritize Impure Rage or Festival of Blood depending on the matchup.",
}

HERO_SPELL = {
    "aldous": "Retribution - he needs jungle farm to scale up quickly.",
    "miya": "Flicker or Inspire - to avoid dives and maximize DPS.",
    "chou": "Flicker - for a flexible engage or escape using the Flicker + Ultimate combo.",
    "alucard": "Retribution if jungling, otherwise Sprint to close gaps quickly in fights.",
    "eudora": "Flameshot or Petrify - for her burst combo.",
    "gusion": "Flicker - for a flexible burst engage on the backline.",
    "ling": "Retribution - he's a jungler, so early farm matters a lot.",
    "fanny": "Retribution - also a jungler, prioritize early practice with cable-cutting and farm.",
    "tigreal": "Flicker - for a surprise engage with his Ultimate.",
    "grock": "Flicker - for an unexpected engage on the backline using his wall combo.",
    "clint": "Flicker or Inspire - to avoid assassin dives.",
    "novaria": "Flameshot or Sprint - to create space before bursting.",
    "lapu lapu": "Retribution if jungling, otherwise Flicker for engages.",
    "aurora": "Flameshot - for long-range poke and securing kills with her Ultimate.",
}

HERO_COUNTERS = {
    "miya": ("gusion", "he can dive her quickly before she deals significant damage."),
    "chou": ("tigreal", "his CC lock disrupts Chou's combo before he can use it."),
    "alucard": ("eudora", "her burst stun interrupts Alucard's sustain playstyle."),
    "aldous": ("fanny", "she can reach Aldous quickly before he stacks up damage."),
    "eudora": ("ling", "he can dive the backline fast before Eudora lands her stun."),
    "gusion": ("grock", "he's tanky against Gusion's burst combo and has CC of his own."),
    "ling": ("tigreal", "his Ultimate has wide CC that catches Ling even while wall-climbing."),
    "fanny": ("eudora", "her ranged stun hits before Fanny can close in with her Cable."),
    "tigreal": ("aurora", "her long range makes it hard for Tigreal to approach without getting CC'd first."),
    "grock": ("eudora", "her burst magic damage overwhelms Grock's defenses."),
    "clint": ("gusion", "he can burst Clint down before Clint gets a basic attack off."),
    "novaria": ("fanny", "she can reach the backline fast before Novaria can combo."),
    "lapu lapu": ("tigreal", "his CC lock disrupts Lapu-Lapu's stance-switch combo."),
    "aurora": ("ling", "he can close the distance fast before Aurora can freeze him."),
}

ROLE_KEYWORDS = {
    "marksman": "Marksman",
    "assassin": "Assassin",
    "mage": "Mage",
    "tank": "Tank",
    "fighter": "Fighter",
    "support": "Support",
}

ROLE_QUESTION_WORDS = ["role", "class", "position", "type", "what class"]

OTHER_HEROES = [
    "balmond", "saber", "alice", "nana", "karina", "akai", "franco", "bane", "bruno",
    "rafaela", "zilong", "layla", "minotaur", "lolita", "hayabusa", "freya", "gord",
    "natalia", "kagura", "sun", "alpha", "ruby", "yi sun shin", "moskov", "johnson",
    "cyclops", "estes", "hilda", "vexana", "roger", "karrie", "gatotkaca", "harley",
    "irithel", "argus", "odette", "lancelot", "diggie", "hylos", "zhask", "helcurt",
    "pharsa", "lesley", "jawhead", "angela", "valir", "martis", "uranus", "hanabi",
    "chang e", "kaja", "selena", "claude", "vale", "leomord", "lunox", "hanzo",
    "belerick", "kimmy", "thamuz", "harith", "minsitthar", "kadita", "faramis",
    "badang", "khufra", "granger", "guinevere", "esmeralda", "terizla", "x borg",
    "dyrroth", "lylia", "baxia", "masha", "wanwan", "silvanna", "cecilion", "carmilla",
    "atlas", "popol", "kupa", "yu zhong", "luo yi", "benedetta", "khaleed", "barats",
    "brody", "yve", "mathilda", "paquito", "gloo", "beatrix", "phoveus", "natan",
    "aulus", "aamon", "valentina", "edith", "floryn", "yin", "melissa", "xavier",
    "julian", "fredrinn", "joy", "arlott", "ixia", "cici", "zhuxin", "chip", "suyou",
    "lukas",
]

ITEM_INFO = {
    "berserker's fury": "Core marksman item. Gives large Physical Attack and Critical Chance, plus bonus Crit Damage when you land a crit.",
    "malefic roar": "Adds Physical Attack and Physical Penetration. Its passive grants extra penetration against high-defense enemies.",
    "windtalker": "Marksman item with Attack Speed, Crit Chance, and a Movement Speed boost whenever a basic attack lands (has a cooldown).",
    "blade of despair": "The largest pure Physical Attack item among marksman items. Its passive adds bonus damage against low-HP enemies.",
    "endless battle": "Gives Attack Speed, Physical Attack, and Mana/Energy regen. Its passive stacks extra attack speed and damage.",
    "wind of nature": "Defensive marksman item, gives HP, Physical Attack, and Attack Speed. Has a damage reduction passive.",
    "haas's claws": "Gives Physical Attack and Lifesteal, with bonus true damage against high-HP enemies.",
    "corrosion scythe": "Physical Attack and Lifesteal item whose passive reduces the enemy's max HP regen.",
    "genius wand": "Mage item with Magic Power and Magic Penetration, penetration increases as the enemy's HP drops.",
    "lightning truncheon": "Magic Power item whose passive sends out chain lightning damage after using a skill.",
    "holy crystal": "The single largest pure Magic Power item, no passive but a straight damage boost.",
    "clock of destiny": "Gives Magic Power, HP, and Mana that grow over the course of the match (item growth).",
    "concentrated energy": "Magic Power and Mana Regen item with a passive shield when your HP is low.",
    "fleeting time": "Gives Magic Power and Cooldown Reduction, with a passive that grants bonus Attack Speed after using a skill.",
    "divine glaive": "Magic Penetration item, penetration percentage scales with the enemy's magic defense.",
    "ice queen wand": "Magic Power item with a skill-slow effect and bonus magic damage against low-HP enemies.",
    "immortality": "Defensive item whose passive revives you with a shield and HP after you die (has a cooldown).",
    "athena's shield": "Gives Magic Defense and HP, with a passive shield against magic damage.",
    "antique cuirass": "Physical Defense item whose passive slows and reduces the attack speed of nearby enemies.",
    "dominance ice": "Defense item that reduces the attack speed and healing effect of enemies.",
    "oracle": "Tank/support item that gives HP regen and HP/Shield boost based on max HP.",
    "radiant armor": "Defense item with a passive that reflects crowd control back onto the enemy.",
    "cursed helmet": "Tank item with a magic damage aura that hurts enemies around you.",
    "brute force breastplate": "Hybrid defense item that gives HP, Physical Defense, and a team-wide Movement/Attack Speed boost when triggered.",
    "warrior boots": "Boots that give Physical Defense, good for fighters and tanks.",
    "tough boots": "Boots with Crowd Control Reduction, useful against CC-heavy enemy teams.",
    "swift boots": "Boots with the highest Movement Speed boost, ideal for marksmen and assassins.",
    "arcane boots": "Boots with Magic Penetration, made for mages.",
    "rose gold meteor": "Support item with Magic Power and a shield that can be shared with a teammate.",
}

SLANG_RESPONSES = {
    "bet": "Bet!  Let's build this the right way.",
    "no cap": "No cap fr fr, that's really the correct build.",
    "cap": "Ay that's cap  that's not the right item build, ask me again.",
    "slay": "Slayyy  that's exactly how you should build it.",
    "rizz": "The rizz on that question, alright let me answer it properly.",
    "sus": "That question is kinda sus but I'll answer it anyway .",
    "mid": "That combo is mid if the build is wrong, so follow this item set instead.",
}

GREETINGS = ["hi", "hello", "hey", "yo", "sup"]
FAREWELLS = ["bye", "goodbye", "see you", "gtg", "later"]

GREETING_REPLIES = [
    "Hey! Ask me about the role, items, or build of any ML hero. ",
    "Hi there! Which hero do you want to talk about?",
    "Hello! I'm ready, who's the hero?",
    "Yo! Let's go, which hero are you asking about?",
]

FAREWELL_REPLIES = [
    "Alright, bye! GG WP, good luck on your next match. ",
    "See you! Take care, let's push rank together next time. ",
    "Okay bye! Hope you win your next ranked game.",
    "Alright, later. GG, take care! ",
]

SMALLTALK = {
    "who are you": "I'm your ML buddy here - ask me about the role, items, or build of any hero (from my limited list).",
    "how are you": "I'm doing fine, how about you? Just tell me which hero you're thinking about.",
    "what are you doing": "Just here waiting for your questions about ML hero items or builds.",
    "thanks": "You're welcome! Ask again if there's anything else you want to know.",
    "thank you": "You're welcome! I'm sure you've got more questions coming, right?",
}

FALLBACKS_SHORT = [
    "Huh?",
    "Wait, what?",
    "Hah, didn't get that.",
    "Say that again?",
    "What was that? ",
]

FALLBACKS_QUESTION = [
    "Hmm, not sure about that one, try asking it more clearly.",
    "I'm not sure about that, maybe try rephrasing it.",
    "Can't answer that right away, say it more specifically.",
    "Hmm, that's a bit unclear to me, try again.",
]

FALLBACKS_GENERAL = [
    "Didn't get that, bro ",
    "Say that again, I missed it.",
    "Okay, but clarify a bit more, I didn't quite catch it.",
    "Whoops, didn't catch that, try again.",
    "Wait, say that again?",
]

TOPIC_REPLIES = {
    "meta": [
        "That changes every patch, depends on who got nerfed or buffed last update.",
        "Meta talk, huh. Usually whichever hero gets banned a lot is in the meta.",
    ],
    "counter": [
        "Depends on the matchup - tell me which hero and I might be able to help.",
        "Counter-picking is a whole topic, but tell me the hero and I'll try to help.",
    ],
    "matchup": [
        "Matchups depend on both heroes - tell me the two heroes so I can answer properly.",
    ],
    "rank": [
        "It's all about the grind, no shortcuts in ranked",
        "Ranked struggles, huh. Solid build first, then consistency.",
    ],
    "emblem": [
        "Depends on the role - marksman/assassin usually run a custom emblem, tank/support is a different setup.",
    ],
    "skin": [
        "Ah, skins are just cosmetic, no effect on stats ",
    ],
    "tier": [
        "Tier lists change every patch too, so don't lean on them too much.",
    ],
    "jungle": [
        "Jungle timing is usually a priority in the early game, but it depends on your hero.",
    ],
    "lane": [
        "Depends whether it's gold lane, exp lane, or mid - item priority differs.",
    ],
    "spell": [
        "Battle spell choice usually depends on the hero's role, tell me who and I might help.",
    ],
}


def find_topic(text):
    for topic, replies in TOPIC_REPLIES.items():
        if topic in text:
            return topic
    return None


def smart_fallback(raw_text, norm_text):
    word_count = len(norm_text.split())
    if word_count <= 2:
        return random.choice(FALLBACKS_SHORT)
    if "?" in raw_text:
        return random.choice(FALLBACKS_QUESTION)
    return random.choice(FALLBACKS_GENERAL)


MISTAKE_REPLIES = [
    "Still not on my list, bro. Try someone else.",
    "I still don't know that hero, sorry. Try a different name.",
    "Really don't have that one, huh. Maybe you know another?",
    "Still not on my list, try a different hero.",
]

ROLE_CORRECT_TEMPLATES = [
    "Yep, you're right! {name} really is {actual}.",
    "Correct! {name} is indeed {actual}.",
    "Yes! Turns out {name} really is {actual}.",
    "Right! {name} is {actual}, you didn't miss.",
]

ROLE_WRONG_TEMPLATES = [
    "Are you dumb? Do you even play ML? {name} is {actual}, not {claimed}.",
    "Nope, wrong! {name} is {actual}, not {claimed}. Back to the tutorial. 💀",
    "Sus, that's wrong. {name} is {actual}, not {claimed}. Clearly you haven't explored the roster.",
    "Nah, wrong. {name} is really {actual}, not {claimed}. It's okay though, ask again.",
]

ROLE_PLAIN_TEMPLATES = [
    "{name} is {actual}.",
    "{name} is a {actual}.",
    "Did you know, {name} is a {actual}.",
    "{actual}, that's what {name} is.",
]

BUILD_NAMES_INTROS = [
    "For {name}, here are the items:",
    "Here's the item list for {name}:",
    "Alright, here's what you should buy for {name}:",
    "For {name}, build this:",
]

BUILD_FULL_INTROS = [
    "{name} ({role}) - here's the item build with attributes:",
    "Okay, here's {name}'s ({role}) full build with each item's attributes:",
    "Here you go, for {name} ({role}), items and attributes:",
]

HERO_LIST_PHRASES = [
    "your heroes", "hero list", "list of heroes", "what heroes do you have",
    "which heroes", "who are your heroes", "how many heroes",
]

CURSE_WORDS = ["stupid", "idiot", "dumb", "fool", "moron", "loser"]

CURSE_COMEBACKS = [
    "You started it, and now I'm the bad guy? Fine, you're stupid too! 😆",
    "Wow, big talk, but that goes right back at you, idiot! 😹",
    "Geez, so rude... it's fine, you're one too HAHAHA",
    "Whoa hold on, is this how you talk? You're dumb too HAHAHA",
]

LOVE_PHRASES = ["i love you", "love you", "i like you", "crush on you"]

LOVE_REPLIES = [
    "Aw HAHAHA, love you too... in item builds! 😂",
    "I love you too, but item builds are really all I know how to give HAHAHA",
    "Aw that's sweet, love you too but let's focus on ML builds first HAHAHA",
    "Whoa that's fast, but sure, love you too HAHAHA - item build next!",
]

_mistake_count = 0


def normalize(text):
    text = text.lower().strip()
    text = text.replace("-", " ").replace(".", " ")
    text = re.sub(r"\s+", " ", text)
    return text


def has_word(text, phrase):
    pattern = r"\b" + re.escape(phrase) + r"\b"
    return re.search(pattern, text) is not None


def find_slang(text):
    matches = [k for k in SLANG_RESPONSES if has_word(text, k)]
    if not matches:
        return None
    matches.sort(key=len, reverse=True)
    return matches[0]


def find_hero(text):
    for hero in HERO_BUILDS:
        if has_word(text, hero):
            return hero
    return None


def find_other_hero(text):
    for name in OTHER_HEROES:
        if has_word(text, name):
            return name
    return None


def find_item(text):
    for item in ITEM_INFO:
        if item in text:
            return item
    return None


def find_smalltalk(text):
    matches = [k for k in SMALLTALK if k in text]
    if not matches:
        return None
    matches.sort(key=len, reverse=True)
    return SMALLTALK[matches[0]]


def hero_display(hero):
    return HERO_DISPLAY.get(hero, hero.title())


def is_build_query(text):
    keywords = ["build", "item", "buy", "what to get", "recommend", "combo", "set"]
    return any(k in text for k in keywords)


def is_role_query(text):
    return any(phrase in text for phrase in ROLE_QUESTION_WORDS)


def is_bare_sino(text):
    return has_word(text, "who")


def wants_attributes(text):
    keywords = [
        "attribute", "attributes", "effect", "stats", "stat",
        "description", "explain", "use", "benefit", "benefits", "bonus",
        "function", "passive", "meaning", "what does it do",
    ]
    return any(k in text for k in keywords)


def is_hero_list_query(text):
    return any(p in text for p in HERO_LIST_PHRASES)


def hero_list_response():
    names = [hero_display(h) for h in HERO_BUILDS]
    return "Here are the heroes on my list: " + ", ".join(names) + "."


def find_curse(text):
    return any(has_word(text, w) for w in CURSE_WORDS)


def find_love(text):
    return any(p in text for p in LOVE_PHRASES)


def role_response(hero, claimed_role=None):
    actual = HERO_ROLES[hero]
    name = hero_display(hero)
    if claimed_role:
        if claimed_role.lower() == actual.lower():
            template = random.choice(ROLE_CORRECT_TEMPLATES)
        else:
            template = random.choice(ROLE_WRONG_TEMPLATES)
        return template.format(name=name, actual=actual, claimed=claimed_role)
    template = random.choice(ROLE_PLAIN_TEMPLATES)
    return template.format(name=name, actual=actual)


def build_names_response(hero):
    items = HERO_BUILDS[hero]
    name = hero_display(hero)
    intro = random.choice(BUILD_NAMES_INTROS).format(name=name)
    lines = [intro]
    for i, item in enumerate(items, 1):
        lines.append(f"  {i}. {item}")
    return "\n".join(lines)


def build_full_response(hero):
    items = HERO_BUILDS[hero]
    role = HERO_ROLES.get(hero, "")
    name = hero_display(hero)
    intro = random.choice(BUILD_FULL_INTROS).format(name=name, role=role)
    lines = [intro]
    for i, item in enumerate(items, 1):
        desc = ITEM_INFO.get(item.lower(), "")
        lines.append(f"  {i}. {item} - {desc}")
    return "\n".join(lines)


def item_response(item):
    desc = ITEM_INFO.get(item, "I don't have info on that one, sorry.")
    return f"{item.title()}: {desc}"


def emblem_response(hero):
    name = hero_display(hero)
    info = HERO_EMBLEM.get(hero, "")
    return f"For {name}: {info}"


def spell_response(hero):
    name = hero_display(hero)
    info = HERO_SPELL.get(hero, "")
    return f"Battle spell for {name}: {info}"


def counter_response(hero):
    name = hero_display(hero)
    counter_hero, reason = HERO_COUNTERS.get(hero, (None, None))
    if not counter_hero:
        return f"I don't have a good counter suggestion for {name} right now."
    counter_name = hero_display(counter_hero)
    return f"{counter_name} is a good counter to {name} - {reason}"


def chatbot_reply(user_text):
    global _mistake_count
    text = normalize(user_text)

    if any(has_word(text, f) for f in FAREWELLS):
        return random.choice(FAREWELL_REPLIES)

    smalltalk = find_smalltalk(text)
    if smalltalk:
        return smalltalk

    if any(has_word(text, g) for g in GREETINGS):
        return random.choice(GREETING_REPLIES)

    banter = ""
    if find_curse(text):
        banter = random.choice(CURSE_COMEBACKS) + " "
    elif find_love(text):
        banter = random.choice(LOVE_REPLIES) + " "

    slang_hit = find_slang(text)
    slang_reply = SLANG_RESPONSES[slang_hit] + " " if slang_hit else ""

    if is_hero_list_query(text):
        return banter + slang_reply + hero_list_response()

    hero = find_hero(text)
    item = find_item(text)

    claimed_role = None
    for role_word, role_name in ROLE_KEYWORDS.items():
        if has_word(text, role_word):
            claimed_role = role_name
            break

    if hero and claimed_role:
        return banter + slang_reply + role_response(hero, claimed_role)

    if hero:
        parts = []
        if item:
            parts.append(item_response(item))
        if wants_attributes(text) and not item:
            parts.append(build_full_response(hero))
        elif is_build_query(text) and not item:
            parts.append(build_names_response(hero))
        if has_word(text, "counter") or "counters" in text:
            parts.append(counter_response(hero))
        if has_word(text, "emblem") or "emblems" in text:
            parts.append(emblem_response(hero))
        if has_word(text, "spell") or "spells" in text:
            parts.append(spell_response(hero))
        if is_role_query(text):
            parts.append(role_response(hero))
        elif is_bare_sino(text) and not parts:
            parts.append(role_response(hero))

        if parts:
            return banter + slang_reply + "\n".join(parts)
        return banter + slang_reply + role_response(hero)

    if item:
        return banter + slang_reply + item_response(item)

    other = find_other_hero(text)
    if other:
        _mistake_count += 1
        if _mistake_count == 1:
            return banter + "Sorry Michael, my hero pool is limited to what's listed."
        return banter + random.choice(MISTAKE_REPLIES)

    topic = find_topic(text)
    if topic:
        return banter + slang_reply + random.choice(TOPIC_REPLIES[topic])

    if banter:
        return banter.strip()

    if slang_hit:
        return slang_reply + "Just tell me which hero or item you want to know about, I'll answer right away."

    return smart_fallback(user_text, text)


def main():
    print("=" * 60)
    print(" ML ITEM BUILD CHATBOT (type 'bye' to exit)")
    print("=" * 60)
    print("Bot: Hey! Ask me about the role, items, or build of any ML hero.")

    while True:
        user_input = input("You: ")
        reply = chatbot_reply(user_input)
        print("Bot:", reply)
        if any(has_word(normalize(user_input), f) for f in FAREWELLS):
            break


if __name__ == "__main__":
    main()
