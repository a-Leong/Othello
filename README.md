# OTHELLO
## Overview
Othello is a fairly simple game to play but can involve highly complex strategies, making it a particularly interesting problem in the context of artificial intelligence. The game is played on an 8-by-8 board. One player plays black tiles, and the other white tiles. The ultimate objective of the game is to fill the board with as many tiles of your color as possible. However, a valid move must “surround” an opponent’s tile(s), either vertically, horizontally, or diagonally. When a player surrounds their opponent’s tile(s), those tiles are flipped to the player’s color.

The primary scope of my contribution included game state and interface development, and AI development including the random algorithm, 
evaluation function, greedy algorithm, and minimax algorithm with alpha-beta pruning.

Created for CS 4701: Artificial Intelligence Practicuum at Cornell University.


## Playing the Game
1. Run main.py without command line arguments to start a two player game.

2. Run main.py with one of the following arguments to start:

    ### ai
    a one player game against AI

    ### randvsrand
    watch a game rand vs rand

    ### basevsbase
    watch a game basicAI vs basicAI
    
    ### basevsab
    watch a game basic AI vs hard AI

3. "exit" may be inputted to kill main.py.
