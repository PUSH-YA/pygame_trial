# Pygame Trial
 My first attempt at making a game from scratch in python using pygame library

 ## Description:
 This a local multiplayer game platformer where the 2 players have different controls and can play against each other where they can move onto different platforms and attack each other. You can choose your own custom name, can change between moving or static backgrounds and can choose between a normal and a "special" mode of gameplay which changes the art theme of the game.

 ## Inspiration:
 I used to play a game similar to the description above on a free game website that has been discontinued (However, there are still games of similar concepts). I wanted to share that experience with my close friends and have made this game. 

## Screenshots of the game:
![image](https://github.com/PUSH-YA/pygame_trial/assets/91928008/a8260cf0-caa2-4473-a7bd-a77d340ffc10)
![image](https://github.com/PUSH-YA/pygame_trial/assets/91928008/2e53cee1-baea-4103-8883-f1ae4ff7f896)
![image](https://github.com/PUSH-YA/pygame_trial/assets/91928008/d5fc76dc-de00-4541-a1b3-d97c0f881870)


## Instructions:
- clone the repo
- run the code for my_game.py`
- There is a separate instructions however `w`,`a`,`d` and `up`,`left` and `right` for movement; `E/Lshift` and `pgup` and `pg down` for attacking and `r` to restart the game
- These buttons can be reprogrammed if needed in code in the `game_loop()` or `playerA_move()` or `playerB_move()`

## What this game helped me learn/improve:
- Reading documentation and implementing your algorithms based on the resources provided (it is a very fundamental skill however, novice coders can improve a lot with practice)
- Testing and debugging (again a foundational skill but more practice makes it better)
- Improved my algorithmic and logical problem solving abilities (several designs might be unorthodox but make the program "work")
- Work with Git and GitHub for version controlling a project
- Game design fundamentals and pixel art
- Learning how to capture dynamic and various types of user input and change the gameplay accordingly
- How to use pygame for different animations in the game (limited in its capability)
- Work with several different audio files in pygame

## Future improvements:
The game is made as a personal project and has been incrementally built from the simple game mechanic to a full game with the menu system. As a result of such game development, the code needs to be heavily reformatted:
- It needs to be reformatted according to the Object Oriented Design principles 
- There are several code blocks with high coupling which makes improving and scaling the game difficult
- The game NEEDS two players to have fun however, another "AI" mode where the enemy will be based on a simplistic script and allow for single player fun.
- Have reprogrammable buttons so, people with any keyboard configurations can play the game (right now you have to do it in the code).
