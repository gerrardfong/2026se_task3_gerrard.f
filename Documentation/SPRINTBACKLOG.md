# SPRINTBACKLOG.md

---

# Sprint 1

## Sprint Goal

Develop the core character creation system, including RNG generation, character management, and frontend navigation.

## Committed Items

- PB-01 User Login System
- PB-03 RNG Character Generation
- PB-04 Character Roll Preview
- PB-06 Rename Character
- PB-07 Delete Character
- PB-08 Edit Profile Image

## Sprint Plan

1. Develop RNG species generation system.
2. Develop RNG attribute generation system.
3. Create character creation frontend.
4. Create navigation and main menu UI.
5. Implement rename and delete character routes.
6. Implement roll preview functionality 

## Unit Test Summary

| Test ID | Test Name | What It Tests | Input | Expected Output | Actual Output | Pass / Fail |
|----------|------------|---------------|---------|-----------------|---------------|-------------|
| T1-01 | User Login | PB-01 User Login authentication | Valid username/password | User redirected to main menu and session created | | |
| T1-02 | Species Roll | PB-03 RNG species generation | Roll request | Random species returned | | |
| T1-03 | Attribute Roll | PB-03 RNG attribute generation | Roll request | Random attributes returned | | |
| T1-04 | Roll Preview | PB-04 Preview generated character | Preview request | Character displayed before saving | | |
| T1-05 | Rename Character | PB-06 Rename functionality | Character ID + new name | Character name updated | | |
| T1-06 | Delete Character | PB-07 Delete functionality | Character ID | Character removed from database | | |
| T1-07 | Profile Image Preview | PB-08 Profile image preview | Uploaded image | Image displayed correctly | | |

## Sprint Review

### Completed
- RNG system completed.
- Character creation interface completed.
- Main menu and navigation bar implemented.
- Roll preview functionality completed.
- Rename and delete character features completed.

### Incomplete
- Profile image editing moved to later sprint.

### Issues Encountered
- PB-04 Roll Preview, client has requested that rolls should be able to be viewed before saving into character. This requires JS in order to store rolls into variables which can altered and viewed on the page (I don't know JS) so I have to discuss with client whether they're fine with rendering the whole page again after rolling or whether they want JS implementation.
- (Fixed) PB-04 Client requested JS implementation so I had to use AI and simplify HTML to the extent where it would only use "ids" and not "onclick" or any other functions
- PB-08 required AI since I wasn't sure how to create the CSS for the pfp picture preview and also needed to be able to accept GIFs format and specific sizing

## Sprint Retrospective

### What Went Well
- Core systems completed quickly.
- Database integration worked as expected.

### Improvements
- Better planning for future feature dependencies.

### Actions for Next Sprint
- Begin progression and combat development.

---

# Sprint 2

## Sprint Goal

Implement progression systems, species buffs and enemy generation required for combat systems.

## Committed Items

- PB-05 Species Buff System
- PB-10 Enemy Generation
- PB-12 XP System
- PB-13 XP Thresholds

## Sprint Plan

1. Add XP tracking to characters.
2. Add rarity thresholds.
3. Develop species buff calculations.
4. Develop enemy generation system.
5. Implement rarity warning popups.
6. Implement popup toggle preferences.

## Unit Test Summary

| Test ID | Test Name | What It Tests | Input | Expected Output | Actual Output | Pass / Fail |
|----------|------------|---------------|---------|-----------------|---------------|-------------|
| T2-01 | Species Buff Application | PB-05 Buff calculation | Generated character | Correct modifiers applied | | |
| T2-02 | XP Storage | PB-12 XP system | XP reward | XP stored successfully | | |
| T2-03 | XP Threshold | PB-13 XP threshold progression | XP value exceeding threshold | Threshold recognised correctly | | |
| T2-04 | Enemy Generation | PB-10 Enemy generation | Generate enemy request | Enemy generated with random attributes | | |
| T2-05 | Roll Confirmation Popup | PB-15 Rarity protection popup | High rarity roll | Warning popup displayed | | |
| T2-06 | Popup Toggle | PB-16 Popup preferences | Toggle setting | Popup behaviour changes correctly | | |

## Sprint Review

### Completed
- Added XP column.
- Added threshold column.
- Implemented species buffs.
- Implemented enemy generation backend.

### Incomplete
- Full gauntlet mode deferred and redirected to Sprint 3

### Issues Encountered
- Sprint priorities changed due to client requests.
- Database structures required redesign.
- Enemies data structure had to be re-evaluated from 

## Sprint Retrospective

### What Went Well
- Database redesign completed successfully.
- Species buff system integrated correctly.

### Improvements
- Reduce sprint scope changes.

### Actions for Next Sprint
- Focus entirely on combat implementation.

---

# Sprint 3

## Sprint Goal

Develop and implement the gauntlet combat system.

## Committed Items

- PB-09 Gauntlet Gamemode
- PB-10 Enemy Generation
- PB-11 Boss Encounters
- PB-12 XP Rewards
- PB-14 Combat System
- PB-11 Boss Encounters
- PB-17 Unlockable Species
- PB-18 Species Unlock Progression

## Sprint Plan

1. Implement endless gauntlet mode.
2. Implement wave-based gauntlet mode.
3. Implement attribute comparison combat.
4. Implement XP rewards.
5. Implement boss encounters.
6. Connect combat to character progression.
7. Implement unlockable species rewards.
8. Create awakened boss system.

## Unit Test Summary

| Test ID | Test Name | What It Tests | Input | Expected Output | Actual Output | Pass / Fail |
|----------|------------|---------------|---------|-----------------|---------------|-------------|
| T3-01 | Endless Mode | PB-09 Endless gauntlet | Start endless run | Enemies continuously generated | | |
| T3-02 | Wave Mode | PB-09 Wave gauntlet | Start wave run | Fixed wave progression generated | | |
| T3-03 | Attribute Combat | PB-14 Combat calculation | Character vs enemy attributes | Correct winner calculated | | |
| T3-04 | XP Reward | PB-12 XP rewards | Enemy defeat | XP added to session total | | |
| T3-05 | XP Save | PB-12 XP persistence | End combat | XP saved to database | | |
| T3-06 | Boss Encounter | PB-11 Boss generation | Boss wave reached | Boss generated correctly | | |
| T3-07 | Battle Outcome | PB-14 Outcome handling | Combat result | Correct win/loss outcome returned | | |
| T3-08 | Boss Unlock Rewards | PB-17 Species unlock rewards | Defeat unlockable boss | Species unlocked successfully | | |
| T3-09 | Locked Species Restriction | PB-18 Locked species control | Generate character | Locked species unavailable | | |
| T3-10 | Awakened Boss Generation | PB-11 Boss progression | Boss encounter trigger | Correct awakened boss generated | | |
| T3-11 | Species Buff Integration | PB-18 New species buffs | Generate unlocked species | Correct buffs applied | | |

## Sprint Review

### Completed
- waves()
- generate_enemy()
- add_xp()
- save_xp()
- attribute_combat()
- battle_outcome()
- Session-based enemy management.
- Added Shinigami species.
- Added Transcendent Being species.
- Added Superhuman species.
- Added Accursed Pact species.
- Added unlockable species architecture.
- Added boss unlock rewards.
- Implemented create_boss().
- Implemented awakened_boss().

### Incomplete
- Leaderboards.
- Combat animations.

### Issues Encountered
- Frontend development slower than backend implementation.

## Sprint Retrospective

### What Went Well
- Core combat systems completed successfully.
- Unlockable species system expanded progression significantly.

### Improvements
- Better frontend planning.

### Actions for Next Sprint
- Pushing endless() to next sprint and refining UI for Gauntlet

---

# Sprint 4

## Sprint Goal

Implement final quality-of-life improvements.

## Committed Items
- PB-19 User Feedback System
- PB-20 UI Optimisation

## Sprint Plan
1. Implement user feedback button.
2. Improve mobile responsiveness.
3. Improve UI consistency.
4. Perform final testing and optimisation.
5. (Added) endless()

## Unit Test Summary

| Test ID | Test Name | What It Tests | Input | Expected Output | Actual Output | Pass / Fail |
|----------|------------|---------------|---------|-----------------|---------------|-------------|
| T4-01 | Feedback Submission | PB-19 User feedback system | Submit feedback | Feedback stored successfully | | |
| T4-02 | Mobile Layout | PB-20 Mobile optimisation | Open application on mobile | Responsive layout displayed | | |

## Sprint Review

### Completed
- Nothing currently

### Incomplete
- To be completed during development.

### Issues Encountered
- Python environment issues between sprint branches.

## Sprint Retrospective

### What Went Well
- N/A

### Improvements
- N/A

### Actions for Future Development
- N/A