# Product Backlog

## Vision

Develop a web-based RPG character generation and combat system that allows users to create unique characters through RNG mechanics, manage their collection, battle enemies in a gauntlet mode, and progress through an XP-based system.

---

## Product Backlog

| ID    | User Story                                                                                                             | Priority | Acceptance Criteria                                             | Status      |
| ----- | ---------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------- | ----------- |
| PB-01 | As a player, I want to create an account so that my characters can be saved.                                           | High     | User can register with a unique username and email.             | Not Started |
| PB-02 | As a player, I want to log into my account so that I can access my saved characters.                                   | High     | User credentials are validated and a session is created.        | Not Started |
| PB-03 | As a player, I want to generate a character using RNG so that each character is unique.                                | High     | Character receives a randomly generated species and attributes. | Not Started |
| PB-04 | As a player, I want to preview character rolls before saving so that I can decide whether to keep them.                | High     | Roll preview displays generated attributes before confirmation. | Not Started |
| PB-05 | As a player, I want species buffs to affect attributes so that species feel unique.                                    | High     | Species modifiers are applied automatically during generation.  | Not Started |
| PB-06 | As a player, I want to rename characters so that I can personalise them.                                               | Medium   | Character name updates successfully in the database.            | Not Started |
| PB-07 | As a player, I want to delete characters so that I can remove unwanted characters.                                     | Medium   | Character is permanently removed from the database.             | Not Started |
| PB-08 | As a player, I want to change profile images so that my characters are visually distinct.                              | Medium   | Uploaded profile image replaces existing image.                 | Not Started |
| PB-09 | As a player, I want to fight enemies in a gauntlet mode so that I can use my characters in combat.                     | High     | Player can select a character and enter combat.                 | Not Started |
| PB-10 | As a player, I want enemies to be randomly generated so that battles remain varied.                                    | High     | Enemy attributes are generated automatically.                   | Not Started |
| PB-11 | As a player, I want bosses to appear periodically so that progression becomes more challenging.                        | Medium   | Bosses appear at predefined milestones.                         | Not Started |
| PB-12 | As a player, I want to gain XP from combat so that my progress is rewarded.                                            | High     | XP is awarded after successful battles.                         | Not Started |
| PB-13 | As a player, I want XP thresholds to determine progression so that stronger characters require more effort to improve. | Medium   | XP thresholds are calculated using rarity data.                 | Not Started |
| PB-14 | As a player, I want combat outcomes to be determined by attributes so that stronger characters perform better.         | High     | Battle results are generated using attribute comparisons.       | Not Started |
| PB-15 | As a player, I want rarity confirmation popups so that I do not accidentally skip valuable rolls.                      | Medium   | Popup appears when a roll exceeds configured rarity levels.     | Not Started |
| PB-16 | As a player, I want rarity popup settings so that I can customise which rolls require confirmation.                    | Low      | User can configure rarity warning preferences.                  | Not Started |

---

# Product Backlog Changelog

| Date       | Change                                   | Reason                                                                        |
| ---------- | ---------------------------------------- | ----------------------------------------------------------------------------- |
| DD/MM/YYYY | Added PB-01 to PB-16                     | Initial backlog created from Phase 1 requirements and Phase 2 specifications. |
| DD/MM/YYYY | Added PB-XX                              | Client requested additional functionality.                                    |
| DD/MM/YYYY | Re-prioritised PB-XX from Medium to High | Required dependency for upcoming sprint.                                      |
| DD/MM/YYYY | Removed PB-XX                            | Requirement no longer aligned with project scope.                             |

---

## Priority Definitions

* High = Core functionality required for MVP.
* Medium = Important functionality that improves user experience.
* Low = Optional enhancements and quality-of-life features.
