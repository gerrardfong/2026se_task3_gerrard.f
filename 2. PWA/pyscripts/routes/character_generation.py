import sqlite3
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

# Layer 1 — Validate/sanitise raw input at the boundary
def parse_character_request(data: dict) -> dict:
    # Validate types, reject unexpected keys, enforce constraints
    ...

# Layer 2 — Business logic (pure, no DB calls)
def generate_character_attributes(species: str, rarity: str) -> dict:
    # Weighted rolls, stat calculations
    ...

# Layer 3 — DB insertion (parameterised queries only)
def insert_character(user_id: int, character: dict) -> int:
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO characters (user_id, name, rarity) VALUES (?, ?, ?)",
        (user_id, character['name'], character['rarity'])
    )