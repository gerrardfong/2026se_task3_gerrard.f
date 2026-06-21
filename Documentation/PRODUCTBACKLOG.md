## PRODUCTBACKLOG.md

## Vision

A RNG-driven character progression game featuring randomly generated characters, turn-based attribute combat, and a gauntlet progression system with unlockable species, XP scaling, and boss encounters. The system prioritises replayability through randomness, structured progression, and unique combat mechanics.

---

## Product Backlog Table

| PB ID | User Story | Priority | Acceptance Criteria | Status |
|------|-------------|----------|---------------------|--------|
| PB-01 | User wants to be able to log in so they can access saved characters | P1 | User authentication creates valid session and redirects to main menu | Done |
| PB-02 | User wants to be able to register an account so they can create and store characters | P1 | New user account is created and stored securely in database | Planned |
| PB-03 | User wants to be able to generate a random character so they can start playing quickly | P1 | Species + attributes are randomly generated | Done |
| PB-04 | User wants to be able to preview rolled character before saving | P1 | Character displayed before DB commit | Done |
| PB-05 | User wants to be able to have species-based buffs affect gameplay | P2 | Buffs correctly modify attributes | Done |
| PB-06 | User wants to be able to rename their character | P1 | Character name updates in database | Done |
| PB-07 | User wants to be able to delete their character | P1 | Character removed from database | Done |
| PB-08 | User wants to be able to edit profile image including GIFs | P3 | Profile images and GIFs upload correctly | Done |
| PB-08 (extended) | User wants to be able to preview profile image/GIFs through cropout circle | P3 | Profile image is able to be displayed correctly with limitations on image size | Done |
| PB-09 | User wants to be able to access gauntlet mode for endless combat progression | P2 | Endless and wave modes function correctly | Done |
| PB-10 | User wants to be able to have enemies generated randomly | P2 | Enemy stats generated randomly per encounter | Done |
| PB-11 | User wants to be able to encounter bosses for progression milestones | P2 | Bosses spawn at defined progression points | Done |
| PB-11 (extended) | Includes awakened boss system | P2 | Advanced boss variant triggers correctly | Done |
| PB-12 | User wants to be able to have XP tracking from combat | P2 | XP is awarded and stored correctly | Done |
| PB-13 | User wants to be able to have XP thresholds for progression | P2 | Level thresholds trigger correctly | Done |
| PB-14 | User wants to be able to use a combat system based on attributes | P2 | Winner determined correctly from attributes | Done |
| PB-15 | User wants to be able to see rarity confirmation popups for high rolls | P3 | Popup triggers on high rarity events | In Progress |
| PB-16 | User wants to be able to toggle popups in settings | P3 | Popup settings persist and apply correctly | In Progress |
| PB-17 | User wants to be able to unlock species through progression | P3 | Species unlock after boss conditions met | Done |
| PB-18 | User wants to be able to have species locked until boss is defeated | P3 | Locked species cannot be selected until unlocked | Done |
| PB-19 | User wants to be able to submit feedback | P4 | Feedback stored successfully | In Progress |
| PB-20 | User wants to be able to access a responsive and optimised UI | P4 | UI adapts to mobile and desktop layouts | In Progress |
---

## Changelog

### 07/06/2026
- Sprint 1 started focusing on core character creation system.
- Implemented RNG system for species and attributes.
- Built main menu UI, navigation bar, and character creation interface.
- Created API routes for:
  - GIF and profile preview handling
  - Character rename and deletion
  - Species and attribute rolling
  - Roll preview before committing to database
- Established core character management workflow (create → preview → save).

---

### 08/06/2026
- Began gauntlet system design and backend planning.
- Designed enemy generation pipeline:
  - `generate_enemy(name, pfp)`
  - `get_enemyname()`
  - `get_enemypfp()`
  - `generate_gauntlet(int)`
- Planned gauntlet UI structure (left: character, right: enemy ladder progression).
- Designed Flask routes for:
  - `display_enemy()`
  - `generate_gauntlet()`
- Considered separate enemy database vs session-based storage.

---

### 08/06/2026 (Later)
- Reprioritised Sprint 2 scope due to system complexity.
- Shifted focus to:
  - species buffs
  - XP thresholds
  - rarity modification prompts
  - enemy generation completion
  - popup modal system for high-rarity rolls
  - popup toggle system
- Introduced XP system design:
  - XP column in character table
  - threshold column in rarity table
  - XP scaling based on enemy difficulty
- Added reroll functionality concept for attribute adjustments.

---

### 09/06/2026
- Updated database structure:
  - Added XP column to characters
  - Added threshold column to rarities

---

### 11/06/2026
- Implemented species buff system:
  - `get_species_buffs()`
  - `apply_species_buffs()`

---

### 12/06/2026
- Began API integration for species buff system.
- Updated `preview_rolls()` to return both raw and modified attributes.
- Preserved `insert_character()` without structural changes.
- Began migration away from JS-driven frontend toward Flask-rendered UI.
- Standardised request handling using `request.form`.

---

### 16/06/2026
- Used agent tooling to repair corrupted Python environment (pip/venv).
- Added JS integrations for:
  - edit-pfp route
  - preview-roll functionality

---

### 18/06/2026
- Adjusted Sprint 2 scope due to ongoing system changes.
- Implemented modal system for high-rarity roll prevention.
- Added popup toggle system for user control.
- Converted enemy generation to dictionary-based system (session storage).
- Began separation of:
  - standard enemies (session-based)
  - bosses (database/hardcoded system)
- Confirmed Sprint 2 completion goals achieved.

---

### 19/06/2026
- Implemented gauntlet backend systems:
  - `endless()` progression mode
  - `waves()` structured progression mode
  - `generate_enemy()` refactor for wave compatibility
  - `add_xp()` session XP tracking
  - `save_xp()` persistence to character
  - `attribute_combat()` attribute comparison system
  - `battle_outcome()` result resolution system

---

### 20/06/2026
- Introduced unlockable species system tied to bosses:
  - Shinigami
  - Transcendent Being
  - Superhuman
  - Accursed Pact
- Updated database schema:
  - unlock_species_id
  - locked status for species system
- Implemented:
  - `create_boss()`
  - `awakened_boss()`
- Began full species progression architecture linked to boss defeats.

---

### 21/06/2026
- Consolidated XP system into unified PB-12 structure.
- Merged enemy generation under PB-10 definition.
- Unified boss logic under PB-11 including awakened variant.
- Confirmed species buff system fully integrated into combat pipeline.
- Marked profile image editing (PB-08) as planned/deferred.
- Updated PB-17 and PB-18 to reflect completed unlock system.
- Marked UI optimisation (PB-20) as in progress due to remaining frontend work.
- Aligned all backlog statuses with Sprint 1–4 implementation evidence.