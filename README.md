# 2026SE_Task3_Gerrard.F
DD/MM/YYYY
7/6/2026
Sprint 1:
Working on the Character Creation section

- Implemented:
    - RNG system
    - UI for mainmenu, navigation bar and character_creation
    - Created functions and api routes 
        - GIFs and pfp preview
        - delete and rename pre-existing characters
        - roll species and attributes
        - preview rolls before commiting to db

Sprint 2:
Working on Gauntlet gamemode where players will be able to use their character in action

- Old Plan:
    - Quality of Life features: 
        - Add a report/feedback button in footer since the app is able to be accessed by users as long as flask is running
        - Add a common theme and update CSS for all pages including signup and login, so it's aesthetically appeasing
        - Optimise layout for Mobile users as well

    - Build the gauntlet:
        - Compromises of different levels that will have randomly generated enemy attributes and characteristics
        - Add a random generator that creates enemies and randomises their statistics
        - Ensure that there is some sort of battle UI or animation which will most likely be imported off of free assets, so it's more entertaining/engaging
        - Player can select a character they want to put into gauntlet
        - Universal leaderboard that all players can see for competitiveness

- New Plan:
    - implementing species_buffs
    - xp thresholds
    - adding the prompt in the case that I want to change the rarities
    - finishing enemy character generation since I've already started it 
    - (added) implement modals/pop-ups that prevent users from roll past high-rarity rolls
    - (added) add a toggle button that disables pop-ups and what rarities can be skipped

Sprint 3:
- Old Plan:
    - Implement Player vs Player
    - Add Offline mode and Quality of life features

- Plan: 
    - Quality of Life features: 
        - Add a report/feedback button in footer since the app is able to be accessed by users as long as flask is running
        - Add a common theme and update CSS for all pages including signup and login, so it's aesthetically appeasing
        - Optimise layout for Mobile users as well

    - Build the gauntlet:
        - Compromises of different levels that will have randomly generated enemy attributes and characteristics
        - Add a random generator that creates enemies and randomises their statistics
        - Ensure that there is some sort of battle UI or animation which will most likely be imported off of free assets, so it's more entertaining/engaging
        - Player can select a character they want to put into gauntlet
        - Universal leaderboard that all players can see for competitiveness


Sprint 4:
- Plan:
    - Implement Player vs Player
    - Add Offline mode and Quality of life features



Development Log:
8/6/2026
1. Identify and begin functions for gauntlet:
    - generate_enemy(name, pfp) - randomly generate attributes for an enemy character
    - increase rarity rates for enemies to increase difficulty
        - get_enemyname() - generates a random name for enemy
        - get_enemypfp() - generates a random pfp for enemy
    - generate_gauntlet(int) - creates a gauntlet depending on the amount of enemies parsed

2. Identify HTML and CSS layout:
    - Plan is to have two containers left side containing a selected character's data, the right having the list of enemies with a descending box size the higher 'level' in the gauntlet they are
    - There will be a large popup that blurs the previous background that was described and allows the user to select a character to fight
    - Possibly create/import victory/defeat animation

3. Identify flask routes:
    - display_enemy() - shows data according to each individual enemy
    - generate_gauntlet()

4. Enemy database:
    - Create a name db and a pfp db that allows functions to pull random images from each
    - Decide whether to merge enemies into character db or create a separate db

8/6/2026 - Later at night:
- I'm thinking about adding an xp system and choosing whether I have to add columns onto character and rarities table
    - add a threshold column which is the required amount of xp to allow players to upgrade their attributes, increases the higher the level, link to rarities table
    - add an xp bar that is attached to character table and increases depending on the amount of enemies that player has eliminated
    - amount of xp scales depending on enemy difficulty

- Add a re-roll function prompt for users to re-roll specific attributes in the case that I decide to change the list of tiers
    - This activates only in specific cases

- Implement species_buffs functions so that they impact character attributes:
    - requires me to reform rarities by adding a level identifier in order to use the species_buff values or I can use the auto-increment id

I've realised that the order in which I get things done will be much more complicated than anticipated due to client requests and reformatting of existing structures. This means that each sprint can't exactly have a defined purpose or feature as it will be constantly changing.

This sprint will most likely be targetted at:
    - implementing species_buffs
    - xp thresholds
    - adding the prompt in the case that I want to change the rarities
    - finishing enemy character generation since I've already started it 

Sprint 3 can be for gauntlet.

9/6/2026
- Complete new database structures:
    - Add xp column to characters
    - Add threshold column to rarities
- Begin development for species_buffs

11/6/2026
- Completed species_buffs compartments:
    - get_species_buffs()
    - apply_species_buffs()

12/6/2026
- Working on implementing API routes for new species_buff functions:
    - Fix returns from preview_rolls() to return original and modified attributes for user accessibility and readability
    - Insert_characters() shouldn't require any adjustments since it inserts data
        - I will use AI to validate its functionality.
- Going to remove AI'D js that is used to operate the character_creation frontend and convert it into pure html anf flask applications
- The odd structuring of the routes due to "data = request.form" is because I'm too lazy to change all the variable names since I'm moving away from js functionality, so instead of rewriting I'll just change the variable name of "data"

Plan for today:
    - Finish API routes and begin converting frontend from being js reliable into html
        - Implement roll button functionality, finalise button functionality, rename character functionality, delete character functionality
        - Update API routes to accept POST methods and change the return for each from jsonify into render/redirect

16/6/2026
- Agent:
    - Used to fix pip since the virtual py environment was corrupt
    - Added JS for according api routes that required it
        - edit-pfp
        - preview-roll

18/6/2026
- Based off of past goals the aim of this sprint has changed slightly
- Used Agent to add JS for roll-preview and modal pop-up
- This sprint will most likely be targetted at:
    - implementing species_buffs
    - xp thresholds
    - adding the prompt in the case that I want to change the rarities
    - finishing enemy character generation since I've already started it 
    - (added) implement modals/pop-ups that prevent users from roll past high-rarity rolls
    - (added) add a toggle button that disables pop-ups and what rarities can be skipped

- Made enemy_generation() return a dict rather than creating a new enemy sql schema
    - Plan is to store enemy dict in session to allow constant generation as the enemies are meant to be generated then deleted when they're defeated
    - Bosses on the otherhand will be hardcoded by me with customised stats and can be pulled from a sql schema when a certain wave is reached in gauntlet
- Finished goals of Sprint 2 as stated above in Sprint 2 targets
- Using Agent to check that this Sprint is safe to merge back into Main

19/6/2026
Feature WIP: Working on backend for gauntlet added functions: 
- endless() stores character, kill, xp and enemy data in session and generates a new enemy after previous one is defeated and continues until character loses, 
- waves() which consists of a fixed amount of enemies with every 5th one being a hardcoded boss, 
- generate_enemy() just a re-instatement of create_enemy() from enemy_generation.py except this function comes with return conditions for waves(), 
- add_xp() which adds xp from enemy to stored total_xp in session, 
- save_xp() adds the stored total_xp to selected character via character_id, 
- attribute_combat() which compares attribute ranks between enemy and character with the higher character being assigned a point to create an accumulative total  
- battle_outcome() which decides what happens to the character depending on the point differentials returned from attribute_combat()

20/6/2026:
- New Feature: Add unique species to bosses that can be unlocked by users
- There's an issue with the python environments for Jupyternb due to creation of new sprint so I'm developing in a new py file dedicated to sql commands

