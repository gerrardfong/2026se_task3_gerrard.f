import sqlite3 as sql
import random
from flask import session
from routes import character_generation as dbChar

db_path = "../databases/characters/characters.db"

# Generated through AI, added some of my own as well
RANDOM_NAMES = {
        "prefixes": [
        # Game tag style
        "Super", "Red", "Cool", "Dark", "Swift",
        "Iron", "Wild", "Neon", "Blaze", "Stone",
        # Medieval/fantasy style
        "Vor", "Kal", "Drak", "Nym", "Zer",
        "Mal", "Ith", "Bal", "Vex", "Aer",
        "Thoth"
    ],
    "suffixes": [
        # Game tag style
        "Storm", "Strike", "Blade", "Fire", "Shadow",
        "Force", "Fang", "Claw", "Bolt", "Edge",
        # Medieval/fantasy style
        "rex", "dith", "ax", "on", "ius",
        "eth", "ak", "orn", "is", "an",
        "eko"
    ],
}

# path for copy and paste: /static/images/enemies/
RANDOM_PFP = [
    "/static/images/enemies/enemy1.png"
]

ENEMY_TIER_WEIGHTS = {
    "Easy": dbChar.RARITY_WEIGHTS,
    "Intermediate": {
    "Common": 30,
    "Uncommon": 30,
    "Rare": 21,
    "Epic": 15,
    "Legendary": 2.5,
    "Mythic": 1,
    "Ultra": 0.5,
},
    "Hard": {
    "Rare": 50,
    "Epic": 25,
    "Legendary": 17.5,
    "Mythic": 5,
    "Ultra": 2.5,
},

    "Impossible": {
    "Epic": 20,
    "Legendary": 40,
    "Mythic": 30,
    "Ultra": 10,
},
}

def get_name() -> str:
    prefix = random.choice(RANDOM_NAMES["prefixes"])
    suffix = random.choice(RANDOM_NAMES["suffixes"])
    if suffix.islower():
        name = prefix + suffix
        return name
    else:
        name = prefix + " " + suffix
        return name

def get_pfp() -> str:
    return random.choice(RANDOM_PFP)

def create_enemy() -> dict:
    user_id = None
    attributes = {}
    