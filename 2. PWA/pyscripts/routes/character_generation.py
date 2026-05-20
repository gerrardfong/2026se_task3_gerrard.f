import sqlite3 as sql
import random
from flask import session

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

def rarity_generation() -> str:
    return random.choices(
        population=list(RARITY_WEIGHTS.keys()),
        weights=list(RARITY_WEIGHTS.values()),
        k=1
    )[0]

def roll_attribute(attribute, character_id) -> str:
    level = rarity_generation()
    conn = sql.connect(db_path)
    conn.execute("INSERT INTO character_attributes (character_id, attribute, level) VALUES (?,?,?)", (character_id, attribute, level,))
    conn.commit()
    conn.close()
    return level

def roll_species() -> int:
    rarity = rarity_generation()
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id FROM species WHERE rarity=? ORDER BY RANDOM() LIMIT 1", (rarity,))
    species = cur.fetchone()
    conn.close()
    return species[0]

def insert_character(name, species_id) -> int:
    user_id = session.get("user_id")
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO characters (name, species_id, user_id) VALUES (?, ?, ?)",
        (name, species_id, user_id)
    )
    conn.commit()
    character_id = cur.lastrowid
    conn.close()
    return character_id

def view_characters() -> list:
    user_id = session.get("user_id")
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("""SELECT c.id, c.name, s.species, ca.attribute, ca.level
                FROM characters c 
                JOIN species s ON s.id = c.species_id 
                LEFT JOIN character_attributes ca ON ca.character_id = c.id
                WHERE c.user_id=?""", (user_id,))
    columns = [col[0] for col in cur.description]
    characters = [dict(zip(columns, row)) for row in cur.fetchall()]
    conn.close()
    return characters

def view_attributes(character_id) -> list:
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT attribute, level FROM characters_attribute WHERE character_id = ?", (character_id,))
    column = [col[0] for col in cur.description]
    attributes = [dict(zip(column, row)) for row in cur.fetchall()]
    return attributes
