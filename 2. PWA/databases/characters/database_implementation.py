import sqlite3 as sql

conn = sql.connect("/workspaces/2026SE_MAJORPROJECT_Gerrard.F/2. PWA/databases/characters/characters.db")
cur = conn.cursor()

SPECIES = [
    ('Human', 'Balanced baseline species with no innate buffs or debuffs.', "Common"),
    ('Elf',   'Ancient race with unmatched speed and battlefield awareness.', "Rare"),
    ('Dwarf', 'Stout warriors of immense durability, but slower on their feet.', "Rare"),
    ('Demon', 'Infernal beings whose raw power far exceeds their mortal counterparts.', "Legendary"),
    ('Angel', 'Celestial warriors with heightened resilience and intellect.', "Legendary"),
    ("Shinigami", "Spiritual guardians who maintain balance between the living and afterlife", "Legendary", 1),
    ("Transcendent Being", "The ones above all else whose presence is unrivalled", "Ultra", 1),
    ("Superhuman", "Born with the natural strength that rivals that of beastial creatures", "Rare", 1),
    ("Accursed Pact", "The determination of your words have separated fables from reality but at the cost of what", "Mythic", 1),
]

BUFFS = [
    ('Demon', 'Strength',   2),
    ('Demon', 'Durability', 1),
    ('Demon', 'Speed',     -1),
    ('Angel', 'Durability', 2),
    ('Angel', 'IQ',         1),
    ('Elf',   'Speed',      1),
    ('Elf',   'BIQ',        1),
    ('Elf',   'Strength',  -1),
    ('Dwarf', 'Durability', 3),
    ('Dwarf', 'Stamina',    1),
    ('Dwarf', 'Speed',     -2),
    ("Shinigami", "Strength", 2),
    ("Shinigami", "Speed", 1),
    ("Shinigami", "Durability", 2),
    ("Transcendent Being", "Strength", 19),
    ("Transcendent Being", "Durability", 19),
    ("Transcendent Being", "IQ", 19),
    ("Transcendent Being", "BIQ", 19),
    ("Superhuman", "Strength", 2),
    ("Superhuman", "Durability", 1),
    ("Superhuman", "IQ", -2),
    ("Accursed Pact", "Strength", 7),
    ("Accursed Pact", "Durability", 7),
    ("Accursed Pact", "Stamina", -10),
    ("Accursed Pact", "BIQ", 7),
]

# Conditional for when I execute file
cur.execute("DROP TABLE IF EXISTS bosses")
cur.execute("DROP TABLE IF EXISTS boss_attributes")

# Create Boss table
cur.execute("""
    CREATE TABLE IF NOT EXISTS bosses (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        species TEXT, 
        pfp TEXT,
        tier TEXT NOT NULL,
        xp INTEGER NOT NULL,
        unlocks_species_id INTEGER REFERENCES species(id)
    )
""")

# Create boss_attribtues table through FKs to reference original boss data
cur.execute("""
    CREATE TABLE IF NOT EXISTS boss_attributes (
        boss_id INTEGER NOT NULL REFERENCES bosses(id),
        attribute TEXT NOT NULL REFERENCES attributes(attribute),
        level TEXT NOT NULL REFERENCES rarities(level),
        PRIMARY KEY (boss_id, attribute)
    )
""")

# View created bosses
cur.execute("SELECT * FROM bosses;")
print(cur.fetchall())

# Creates new table for users that defines what species that have access to through roll_species()
cur.execute("""
    CREATE TABLE IF NOT EXISTS unlocked_species (
        user_id INTEGER NOT NULL REFERENCES users(id),
        species_id INTEGER NOT NULL REFERENCES species(id),
        PRIMARY KEY (user_id, species_id)
    )
""")
conn.commit()

# Add new column to species that defines whether they're able to use a species, 
# species will contain all species and unlocked_species is what users can roll from
# Already implemented
    # cur.execute("ALTER TABLE species ADD COLUMN locked INTEGER NOT NULL DEFAULT 0")
    # conn.commit()

# Insert boss data into tables including their awakened and unawakened forms
cur.executemany(
    "INSERT OR IGNORE INTO bosses VALUES (?, ?, ?, ?, ?, ?, ?)",
    [
        (1, "Aizen", "Shinigami", "/static/images/bosses/aizen.png", "Hard", 70, None),
        (2, "Aizen_awakened", "Trascendent Being", "/static/images/bosses/aizenawk.png", "Impossible", 150, None),
        (3, "Gon", "Superhuman", "/static/image/bosses/gon.png", "Intermediate", 20, None),
        (4, "Gon_awakened", "Accursed Pact", "/static/image/bosses/gonawk.gif", "Hard", 60, None)
    ]
)

# Insert boss attributes into according bosses
cur.executemany(
    "INSERT OR IGNORE INTO boss_attributes VALUES (?, ?, ?)",
    [
        # Aizen
        (1, "Strength", "Galaxy"),
        (1, "Durability", "Planet"),
        (1, "Stamina", "Continental"),
        (1, "Speed", "Star"),
        (1, "IQ", "Solar System"),
        (1, "BIQ", "Country"),
        # Aizen_awakened
        (2, "Strength", "Universal"),
        (2, "Durability", "Multiversal"),
        (2, "Stamina", "Outerversal"),
        (2, "Speed", "Universal"),
        (2, "IQ", "Absolute"),
        (2, "BIQ", "Multiversal"),
        # Gon
        (3, "Strength", "Island"),
        (3, "Durability", "City"),
        (3, "Stamina", "Mountain"),
        (3, "Speed", "Island"),
        (3, "IQ", "Athletic"),
        (3, "BIQ", "Average"),
        # Gon_awakened
        (4, "Strength", "Planet"),
        (4, "Durability", "Continental"),
        (4, "Stamina", "Country"),
        (4, "Speed", "Planet"),
        (4, "IQ", "Building"),
        (4, "BIQ", "City"),
    ]
)
conn.commit()

# Insert new species into species table
for name, description, rarity, *locked in SPECIES:
    cur.execute(
        "INSERT OR IGNORE INTO species (species, description, rarity, locked) VALUES (?, ?, ?, ?)",
        (name, description, rarity, locked[0] if locked else 0)
    )

for species_name, attribute, modifier in BUFFS:
    cur.execute(
        """INSERT OR IGNORE INTO species_buffs (species_id, attribute, level_modifier)
           VALUES ((SELECT id FROM species WHERE species = ?), ?, ?)""",
        (species_name, attribute, modifier)
    )
conn.commit()

cur.execute(
    "SELECT * FROM species s JOIN species_buffs sb ON s.id = sb.species_id;"
)

for row in cur.fetchall():
    print(row)


conn.close()



