import sqlite3 as sql
import random
from flask import session
from routes import enemy_generation as dbChar

db_path = "../databases/characters/characters.db"

ATTRIBUTES = ["Strength", "Durability", "Stamina", "Speed", "IQ", "BIQ"]

# Gamemode
def endless(character_id: int):
    session["gauntlet"] ={
        "user_id": session.get("user_id"),
        "mode": "endless",
        "character_id": character_id,
        "kills": 0,
        "total_xp": 0,
        "current_enemy": generate_enemy()
    }

# Gamemode
def waves(character_id: int, total_waves: int):
    max_waves = 10
    total_waves = min(total_waves, max_waves)
    session["gauntlet"] = {
        "user_id": session.get("user_id"),
        "mode": "waves",
        "character_id": character_id,
        "kills": 0,
        "total_xp": 0,
        "current_wave": 1,
        "current_enemy": generate_enemy(),
        "total_waves": total_waves
    }
    

# Creates enemy for waves and endless
def generate_enemy():
    current_wave = session["gauntlet"]["current_wave"]
    if current_wave % 5:
        return dbChar.create_boss()
    return dbChar.create_enemy()

# Adds xp from enemy to player when a character defeats the enemy
def add_xp():
    enemy_xp = session["gauntlet"]["current_enemy"]["xp"]
    session["gauntlet"]["total_xp"] += enemy_xp
    session.modified = True

def save_xp():
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
            UPDATE characters SET xp = xp + ? WHERE id = ?,
        """,
        (session["gauntlet"]["total_xp"], session["gauntlet"]["character_id"])
    )

def attribute_combat():
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT attribute, level FROM character_attributes WHERE character_id=?",
        (session["gauntlet"]["character_id"],)
    )
    rows = cur.fetchall()
    character_attributes = {row[0]: row[1] for row in rows}

    cur.execute(
        "SELECT level, rank FROM rarities"
    )
    ranks = cur.fetchall()

    enemy_attributes = session["gauntlet"]["current_enemy"]["attributes"]
    character_points = 0
    enemy_points = 0

    for attr in ATTRIBUTES:
        character_level = ranks[character_attributes[attr]]
        enemy_level = ranks[enemy_attributes[attr]["level"]]
        if character_level > enemy_level:
            character_points += 1
        if character_level < enemy_level:
            enemy_points += 1
    
    return character_points, enemy_points


def battle_outcome() -> str:
    character_points, enemy_points = attribute_combat()

    if character_points > enemy_points:
        add_xp()
        session['gauntlet']['kills'] += 1
        current_enemy = session["gauntlet"]["current_enemy"]

        if current_enemy["is_boss"]:
            awakened = dbChar.awakened_boss(current_enemy["name"])
            if awakened:
                session["gauntlet"]["current_enemy"] = awakened
                session.modified = True
                return "boss_awakened"         
            if current_enemy["unlocks_species_id"]:
                unlock_species(current_enemy["unlocks_species_id"])

        if session['gauntlet']['mode'] == 'waves':
            session['gauntlet']['current_wave'] += 1
            if session['gauntlet']['current_wave'] > session['gauntlet']['total_waves']:
                session.modified = True
                return 'win'

        session['gauntlet']['current_enemy'] = generate_enemy()
        session.modified = True
        return 'character_win'

    elif enemy_points > character_points:
        return 'game_over'

    else:
        session['gauntlet']['current_enemy'] = generate_enemy()
        session.modified = True
        return 'draw'

def unlock_species(unlocks_species_id: int):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO unlocked_species VALUES (?,?)",
        (session["gauntlet"]["user_id"], unlocks_species_id)
    )
    conn.commit()
    conn.close()