import sqlite3 as sql
import random

db_path = "../databases/rarities/characters.db"

RARITY_WEIGHTS = {
    'Common':    40,
    'Uncommon':  25,
    'Rare':      15,
    'Epic':       9,
    'Legendary':  5,
    'Mythic':     4,
    'Ultra':      2,
}

def rarity_generation():
    return random.choices(
        population=list(RARITY_WEIGHTS.keys()),
        weights=list(RARITY_WEIGHTS.values()),
        k=1
    )[0]

def roll_attribute(attribute, character_id):
    level = rarity_generation()
    conn = sql.connect(db_path)
    conn.execute("INSERT INTO character_attributes (character_id, attribute, level) VALUES (?,?,?)", (character_id, attribute, level,))
    conn.commit()
    conn.close()
    return level

def roll_species():
    rarity = rarity_generation()
    conn = sql.connect(db_path)
    cur = conn.cursor()
    conn.execute("SELECT id FROM species WHERE rarity=? ORDER BY RANDOM() LIMIT 1", (rarity))
    user_id = cur.fetchone()
    conn.close()
    return user_id[0]

def insert_character(user_id, character):
    conn = sql.connect(db_path)
    conn.execute(
        "INSERT INTO characters (user_id, name, rarity) VALUES (?, ?, ?)",
        (user_id, character['name'], character['rarity'])
    )

