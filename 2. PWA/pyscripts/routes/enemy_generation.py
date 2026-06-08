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

def create_enemy(name: str, pfp: str) -> dict:
    attributes = 