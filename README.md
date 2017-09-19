# OTHELLO
## Final Project for CS4701

## Overview
### Othello is a fairly simple game to play but can involve highly complex strategies, making it a particularly interesting problem in the context of artificial intelligence. The game is played on an 8-by-8 board. One player plays black tiles, and the other white tiles. The ultimate objective of the game is to fill the board with as many tiles of your color as possible. However, a valid move must “surround” an opponent’s tile(s), either vertically, horizontally, or diagonally. When a player surround their opponent’s tile(s), they are flipped to the player’s color.

### My partner and I began with a random player, then moved on to an evolutionary greedy player (using a more sophisticated evaluation function). After that, we developed a minimax algorithm, and later added alpha-beta pruning for increased efficiency. Furthermore, we implemented a Monte Carlo tree search algorithm. Finally, we created a neural network that uses Q-learning.


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
