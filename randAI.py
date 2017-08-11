"""
RANDOM AI MODULE

BJORNSSON & LEONG PRESENT: IN THE MOOD FOR LOVE: A GAME
CS4701 2017sp
"""

import state as s
import random as r


_BLACK = " X"
_WHITE = " 0"
_EMPTY = "  "


# places a tile on a square chosen at random from available moves.
# AI move functions return True to maintain game loop.
# (if a human player inputs a quit command, move returns False)
def makeMove(board, color):
    if color == _BLACK:
        board.bPosMoves = board.allMoves(_BLACK)
        numMoves = len(board.bPosMoves)

        if numMoves == 0:
            return

        else: 
            moveNum = r.randint(0, numMoves - 1)
            x, y = board.bPosMoves[moveNum]

            board.place(x,y, _BLACK)
            return

    else:
        board.wPosMoves = board.allMoves(_WHITE)
        numMoves = len(board.wPosMoves)

        if numMoves == 0:
            return
        else:
            moveNum = r.randint(0, numMoves - 1)
            x, y = board.wPosMoves[moveNum]
            board.place(x,y, _WHITE)
            return