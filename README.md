# 2026SE_Task3_Gerrard.F

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

Development Goals:
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

Sprint 3:
- Plan:
    - Implement Player vs Player
    - Add Offline mode and Quality of life features