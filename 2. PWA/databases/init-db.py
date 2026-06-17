import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)


def init_users_db():
    db = os.path.join(BASE_DIR, "users", "users.db")
    conn = sqlite3.connect(db)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def init_client_feedback_db():
    db = os.path.join(BASE_DIR, "client_feedback", "client_feedback.db")
    conn = sqlite3.connect(db)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS client_feedback(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            email TEXT NOT NULL,
            types TEXT NOT NULL,
            feedback TEXT
        );
    """)
    conn.commit()
    conn.close()


def init_characters_db():
    db = os.path.join(BASE_DIR, "characters", "characters.db")
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS attributes(
            attribute TEXT PRIMARY KEY
        );
    """)
    cur.executemany(
        "INSERT OR IGNORE INTO attributes VALUES (?)",
        [("Strength",), ("Durability",), ("Stamina",), ("Speed",), ("IQ",), ("BIQ",)],
    )

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rarities (
            level TEXT PRIMARY KEY,
            rarity TEXT NOT NULL,
            rank INTEGER
        );
    """)
    cur.executemany(
        "INSERT OR IGNORE INTO rarities (level, rarity, rank) VALUES (?, ?, ?)",
        [
            ("Useless", "Legendary", 0),
            ("Subhuman", "Rare", 1),
            ("Chudlite", "Rare", 2),
            ("Average", "Common", 3),
            ("Athletic", "Common", 4),
            ("Building", "Uncommon", 5),
            ("City", "Rare", 6),
            ("Mountain", "Rare", 7),
            ("Island", "Epic", 8),
            ("Country", "Epic", 9),
            ("Continental", "Epic", 10),
            ("Planet", "Legendary", 11),
            ("Star", "Legendary", 12),
            ("Solar System", "Legendary", 13),
            ("Galaxy", "Legendary", 14),
            ("Universal", "Mythic", 15),
            ("Multiversal", "Mythic", 16),
            ("Outerversal", "Ultra", 17),
            ("Absolute", "Ultra", 18),
        ],
    )

    cur.execute("""
        CREATE TABLE IF NOT EXISTS species (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            species TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            rarity TEXT NOT NULL DEFAULT 'Common'
        );
    """)
    cur.executemany(
        "INSERT OR IGNORE INTO species (species, description, rarity) VALUES (?, ?, ?)",
        [
            (
                "Human",
                "Balanced baseline species with no innate buffs or debuffs.",
                "Common",
            ),
            (
                "Demon",
                "Infernal beings whose raw power far exceeds their mortal counterparts.",
                "Rare",
            ),
            (
                "Angel",
                "Celestial warriors with heightened resilience and intellect.",
                "Rare",
            ),
            (
                "Elf",
                "Ancient race with unmatched speed and battlefield awareness.",
                "Uncommon",
            ),
            (
                "Dwarf",
                "Stout warriors of immense durability, but slower on their feet.",
                "Uncommon",
            ),
        ],
    )

    cur.execute("""
        CREATE TABLE IF NOT EXISTS species_buffs (
            species_id INTEGER NOT NULL REFERENCES species(id),
            attribute TEXT NOT NULL REFERENCES attributes(attribute),
            level_modifier INTEGER NOT NULL,
            PRIMARY KEY (species_id, attribute)
        );
    """)
    buffs = [
        ("Demon", "Strength", 2),
        ("Demon", "Durability", 1),
        ("Demon", "Speed", -1),
        ("Angel", "Durability", 2),
        ("Angel", "IQ", 1),
        ("Elf", "Speed", 1),
        ("Elf", "BIQ", 1),
        ("Elf", "Strength", -1),
        ("Dwarf", "Durability", 3),
        ("Dwarf", "Stamina", 1),
        ("Dwarf", "Speed", -2),
    ]
    cur.executemany(
        """INSERT OR IGNORE INTO species_buffs (species_id, attribute, level_modifier)
           VALUES ((SELECT id FROM species WHERE species = ?), ?, ?)""",
        buffs,
    )

    cur.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species_id INTEGER NOT NULL REFERENCES species(id),
            user_id INTEGER,
            profile_image TEXT,
            xp INTEGER DEFAULT 0
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS character_attributes (
            character_id INTEGER NOT NULL REFERENCES characters(id),
            attribute TEXT NOT NULL REFERENCES attributes(attribute),
            level TEXT NOT NULL REFERENCES rarities(level),
            PRIMARY KEY (character_id, attribute)
        );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_users_db()
    init_client_feedback_db()
    init_characters_db()
    print("All databases initialised.")
