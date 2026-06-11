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

Sprint 3:
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