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
        "current_wave": 1,
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
        "current_enemy": generate_enemy(1),
        "total_waves": total_waves
    }

def generate_enemy(current_wave=None):
    if current_wave is None:
        current_wave = session["gauntlet"]["current_wave"]
    if current_wave % 5 == 0:
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
        UPDATE characters SET xp = xp + ? WHERE id = ?
        """,
        (session["gauntlet"]["total_xp"], session["gauntlet"]["character_id"])
    )
    conn.commit()
    conn.close()

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
    ranks = {row[0]: row[1] for row in cur.fetchall()}

    enemy_attributes = session["gauntlet"]["current_enemy"]["attributes"]
    character_points = 0
    enemy_points = 0
    breakdown = {}

    for attr in ATTRIBUTES:
        character_level = ranks[character_attributes[attr]]
        enemy_level = ranks[enemy_attributes[attr]["level"]]
        if character_level > enemy_level:
            breakdown[attr] = "character"
            character_points += 1
        elif character_level < enemy_level:
            breakdown[attr] = "enemy"
            enemy_points += 1
        else:
            breakdown[attr] = "draw"
        
    return character_points, enemy_points, breakdown
    


def battle_outcome() -> str:
    character_points, enemy_points, breakdown = attribute_combat()

    if character_points > enemy_points:
        add_xp()
        session['gauntlet']['kills'] += 1
        current_enemy = session["gauntlet"]["current_enemy"]

        if current_enemy.get("is_boss"):
            awakened = dbChar.awakened_boss(current_enemy["name"])
            if awakened:
                session["gauntlet"]["current_enemy"] = awakened
                session.modified = True
                return "boss_awakened", breakdown      
            if current_enemy["unlocks_species_id"]:
                unlock_species(current_enemy["unlocks_species_id"])

        if session['gauntlet']['mode'] == 'waves':
            session['gauntlet']['current_wave'] += 1
            if session['gauntlet']['current_wave'] > session['gauntlet']['total_waves']:
                session.modified = True
                save_xp()
                return 'win', breakdown
        
        session['gauntlet']['current_enemy'] = generate_enemy()
        session.modified = True
        return 'character_win', breakdown

    elif enemy_points > character_points:
        save_xp()
        return 'game_over', breakdown

    else:
        session['gauntlet']['current_enemy'] = generate_enemy()
        session.modified = True
        return 'draw', breakdown

def unlock_species(unlocks_species_id: int):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO unlocked_species VALUES (?,?)",
        (session["gauntlet"]["user_id"], unlocks_species_id)
    )
    conn.commit()
    conn.close()