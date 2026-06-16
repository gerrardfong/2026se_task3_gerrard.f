import sqlite3 as sql
import random
from flask import session

db_path = "../databases/characters/characters.db"

RARITY_WEIGHTS = {
    "Common": 60,
    "Uncommon": 15,
    "Rare": 10,
    "Epic": 6,
    "Legendary": 2.5,
    "Mythic": 1,
    "Ultra": 0.5,
}

ATTRIBUTES = ["Strength", "Durability", "Stamina", "Speed", "IQ", "BIQ"]


def rarity_generation() -> dict:
    rarity = random.choices(
        population=list(RARITY_WEIGHTS.keys()),
        weights=list(RARITY_WEIGHTS.values()),
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


def roll_attribute(attribute, character_id) -> str:
    roll = rarity_generation()
    conn = sql.connect(db_path)
    conn.execute(
        "INSERT INTO character_attributes (character_id, attribute, level) VALUES (?,?,?)",
        (
            character_id,
            attribute,
            roll["level"],
        ),
    )
    conn.commit()
    conn.close()
    return roll


def roll_species() -> tuple:
    rarity = rarity_generation()
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM species WHERE rarity=? ORDER BY RANDOM() LIMIT 1",
        (rarity["rarity"],),
    )
    species = cur.fetchone()
    conn.close()
    return species[0]


def insert_character(name: str, species_id: int , attributes: dict, profile_image: str = None,  user_id: int = "user") -> int:
    if user_id == "user":
        user_id = session.get("user_id")
    profile_image = profile_image or "/static/icons/default_pfp.png"
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM characters WHERE name=? AND user_id=?", (name, user_id))
    if cur.fetchone():
        conn.close()
        return None
    cur.execute(
        "INSERT INTO characters (name, species_id, user_id, profile_image) VALUES (?, ?, ?, ?)",
        (name, species_id, user_id, profile_image),
    )
    character_id = cur.lastrowid
    if attributes:
        cur.executemany(
            "INSERT INTO character_attributes (character_id, attribute, level) VALUES (?,?,?)",
            [(character_id, attr, roll["level"]) for attr, roll in attributes.items()],
        )
    conn.commit()
    conn.close()
    #condition added to make function look tidier 
    if attributes:
        apply_species_buffs(species_id, character_id, "insert")
    return character_id


def view_characters() -> list:
    user_id = session.get("user_id")
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """SELECT c.id, c.name, c.profile_image, c.species_id, s.species, s.rarity, ca.attribute, ca.level, r.rarity
                FROM characters c 
                JOIN species s ON s.id = c.species_id 
                LEFT JOIN character_attributes ca ON ca.character_id = c.id
                LEFT JOIN rarities r ON r.level = ca.level
                WHERE c.user_id=?""",
        (user_id,),
    )
    rows = cur.fetchall()
    conn.close()

    grouped = {}
    for row in rows:
        character_id, name, profile_image, species_id, species, species_rarity, attribute, level, rarity = row
        buffs = get_species_buffs(species_id)
        if character_id not in grouped:
            grouped[character_id] = {
                "id": character_id,
                "name": name,
                "species": species,
                "species_rarity": species_rarity,
                "profile_image": profile_image,
                "buffs": buffs,
                "attributes": [],
            }

        grouped[character_id]["attributes"].append(
            {
                "attribute": attribute,
                "level": level,
                "rarity": rarity,
            }
        )

    return list(grouped.values())


def preview_roll() -> dict:
    """Roll a random species and all attributes without persisting to the DB."""
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, species FROM species ORDER BY RANDOM() LIMIT 1")
    row = cur.fetchone()
    conn.close()
    species_id = row[0]
    species_name = row[1]
    #rolls for attributes
    original_attributes = {attr: rarity_generation() for attr in ATTRIBUTES}
    #applies modifiers onto attributes if there are any 
    attributes = apply_species_buffs(species_id, None, "preview", original_attributes)
    session["pending_roll"] = {
        "species_id": species_id,
        "species": species_name,
        "original_attributes": original_attributes,
        "attributes": attributes,
    }
    return session["pending_roll"]


def rename_character(character_id: int, new_name: str) -> str:
    new_name = (new_name or "").strip()
    if not new_name:
        return False

    user_id = session.get("user_id")
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM characters WHERE user_id = ? AND name = ? AND id<>?",
        (user_id, new_name, character_id),
    )
    if cur.fetchone():
        conn.close()
        return "duplicate"

    cur.execute(
        "UPDATE characters SET name = ? WHERE user_id = ? AND id = ?",
        (new_name, user_id, character_id),
    )
    conn.commit()
    # Validity check to see whether a row was changed or not
    updated = cur.rowcount > 0
    conn.close()
    return "success" if updated else "not_found"


def edit_pfp(pfp: str, character_id: int) -> str:
    user_id = session.get("user_id")
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "UPDATE characters SET profile_image=? WHERE user_id=? AND id=?",
        (pfp, user_id, character_id),
    )
    conn.commit()
    updated = cur.rowcount > 0
    conn.close()
    return "success" if updated else "invalid"


def delete_character(character_id: int) -> str:
    user_id = session.get("user_id")
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM characters WHERE user_id=? AND id=?", (user_id, character_id)
    )
    updated = cur.rowcount > 0
    if updated:
        cur.execute(
            "DELETE FROM character_attributes WHERE character_id=?", (character_id,)
        )
        conn.commit()
    conn.close()
    return "success" if updated else "invalid"

def get_species_buffs(species_id: int) -> dict:
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT attribute, level_modifier FROM species_buffs WHERE species_id=?",(species_id,)
    )
    results = cur.fetchall()
    conn.close()
    # Should build a dict in the format of: {"Strength": "2"}
    return {row[0]: row[1] for row in results}

def apply_species_buffs(species_id: int, character_id: int, mode=None, attributes=None):
    buffs = get_species_buffs(species_id)
    if mode == "insert":
        conn = sql.connect(db_path)
        cur = conn.cursor()
        cur.executemany(
        """UPDATE character_attributes SET level= MAX(1, MIN(19, level+?)) WHERE attribute=? AND character_id=?""",
        [(modifier, attribute, character_id) for attribute, modifier in buffs.items()]
        )
        if cur.rowcount > 0:
            conn.commit()
            conn.close()
            return "updated"
        else:
            conn.close()
            return "human"
    if mode == "preview":
        for attribute, modifier in buffs.items():
            if attribute in attributes:
                attributes[attribute]["level"] = max(1, min(19, attributes[attribute]["level"] + modifier))
        return attributes


def xp_gain():
    pass

def levelup_attribute():
    pass


# REDUNDANT - stored in case of future usage
# def view_attributes(character_id: int) -> list:
#     conn = sql.connect(db_path)
#     cur = conn.cursor()
#     cur.execute(
#         "SELECT attribute, level FROM character_attributes WHERE character_id = ?",
#         (character_id,),
#     )
#     column = [col[0] for col in cur.description]
#     attributes = [dict(zip(column, row)) for row in cur.fetchall()]
#     conn.close()
#     return attributes
