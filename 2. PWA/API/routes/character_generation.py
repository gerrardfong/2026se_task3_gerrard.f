import sqlite3

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
    # Normalise weights to percentages
    total = sum(RARITY_WEIGHTS.values())
    rarity_pct = {rarity: round(weight / total * 100) for rarity, weight in RARITY_WEIGHTS.items()}

    # Attach percentages to each level from the DB
    conn = sqlite3.connect('characters.db')
    rows = conn.execute("SELECT level, rarity FROM rarities").fetchall()

    for level, rarity in rows:
        pct = rarity_pct.get(rarity, 0)
        print(f"{level} [{rarity}] — {pct}%")

    conn.close()

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
    conn = sqlite3.connect('characters.db')
    conn.execute(
        "INSERT INTO characters (user_id, name, rarity) VALUES (?, ?, ?)",
        (user_id, character['name'], character['rarity'])
    )
    ...