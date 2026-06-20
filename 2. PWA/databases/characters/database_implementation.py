import sqlite3 as sql

conn = sql.connect("characters.db")
cur = conn.cursor()

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
# cur.execute("ALTER TABLE species ADD COLUMN locked INTEGER NOT NULL DEFAULT 0")
# conn.commit()

# Insert boss data into tables including their awakened and unawakened forms
cur.executemany(
    "INSERT OR IGNORE INTO bosses VALUES (?, ?, ?, ?, ?, ?, ?)",
    [
        (1, "Aizen", "Shinigami", "/static/images/bosses/aizen.png", "Hard", 70, None),
        (2, "Aizen_awakened", "Shinigami", "/static/images/bosses/aizenawk.png", "Impossible", 150, None),
        (3, "Gon", "Superhuman", "/static/image/bosses/gon.png", "Intermediate", 20, None),
        (4, "Gon_awakened", "Superhuman", "/static/image/bosses/gonawk.gif", "Hard", 60, None)
    ]
)
conn.commit()

conn.close()


