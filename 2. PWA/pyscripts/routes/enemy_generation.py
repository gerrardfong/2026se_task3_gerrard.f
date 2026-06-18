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

TIER_VALUES = {
    "Easy": {"weight": 50 , "xp": 1},
    "Intermediate": {"weight": 35, "xp": 25},
    "Hard": {"weight": 15, "xp": 50},
    "Impossible": {"weight": 5, "xp": 100},
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


def get_tier():
    tier = random.choices(
        population=list(TIER_VALUES.keys()),
        weights=[Tier["weight"] for Tier in TIER_VALUES.values()],
        k=1
    )[0]
    return tier

def rarity_generation(tier="Easy") -> dict:
    rarity = random.choices(
        population=list(ENEMY_TIER_WEIGHTS[tier].keys()),
        weights=list(ENEMY_TIER_WEIGHTS[tier].values()),
        k=1,
    )[0]
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT level FROM rarities WHERE rarity=? ORDER BY RANDOM() LIMIT 1", (rarity,)
    )
    row = cur.fetchone()
    conn.close()
    return {"rarity": rarity, "level": row[0]}

def roll_species() -> tuple:
    rarity = dbChar.rarity_generation()
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM species WHERE rarity=? ORDER BY RANDOM() LIMIT 1",
        (rarity["rarity"],),
    )
    species = cur.fetchone()
    conn.close()
    return species[0]


def create_enemy() -> dict:
    #Enemies should contain a specific xp value depending on their enemy tier
    name = get_name()
    pfp = get_pfp()
    tier = get_tier()
    xp = TIER_VALUES[tier]["xp"]
    species = roll_species()
    attributes = {attr : rarity_generation(tier) for attr in dbChar.ATTRIBUTES}
    attributes = dbChar.apply_species_buffs(species, None , "enemy", attributes)
    buffs = dbChar.get_species_buffs(species)
    enemy = {
        "name": name,
        "pfp": pfp,
        "species": species,
        "tier": tier,
        "xp": xp,
        "buffs": buffs,
        "attributes": attributes
    }
    return enemy
    