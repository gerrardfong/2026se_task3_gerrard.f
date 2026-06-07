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