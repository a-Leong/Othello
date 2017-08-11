"""
ALPHA BETA AI MODULE

BJORNSSON & LEONG PRESENT: IN THE MOOD FOR LOVE: A GAME
CS4701 2017sp
"""


import state as s
import basicAI as b
import copy as c


_BLACK = " X"
_WHITE = " 0"
_EMPTY = "  "

# weights : cornerAdjacency, points, corners, mobility, frontier, stability
_GREEDY_DEFAULT = [382.0, 10.0, 801.0, 79.0, 75.0, 10.0]
_GREEDY_AGGRO =  [549.0, 33.0, 625.0, 103.0, 145.0, 75.0]
_GREEDY_BALANCED = [258.9, 0, 595.6, 66.1, 43.8, 17.0]

_AB_DEFAULT = [451.59, 286.32, 856.17, 609.48, 126.05, 201.12]


#for even numbers, call miniMax to choose move // for odd numbers, call maxiMin to choose move
_ALPHA_BETA_SEARCH_DEPTH = 3


def miniMax(board, color, depth, alpha, beta, level = 0, weights = _GREEDY_BALANCED):
	bestMove = None
	if depth == level:
		return None, b.eval(board, color, weights)
	else:
		if color == _BLACK:
			board.bPosMoves = board.allMoves(_BLACK)
			val = -9999999
			for m in range(len(board.bPosMoves)):
				x, y = board.bPosMoves[m]
				testBoard = c.deepcopy(board)
				testBoard.place(x,y, _BLACK)

				move, tval = maxiMin(testBoard, _WHITE, depth, alpha, beta, level + 1)

				if tval > val:
					val = tval
					bestMove = x,y
				if val >= beta:
					return bestMove, val
				alpha = max(alpha, val)
			return bestMove, val

		else:
			board.wPosMoves = board.allMoves(_WHITE)
			val = -9999999
			for m in range(len(board.wPosMoves)):
				x, y = board.wPosMoves[m]
				testBoard = c.deepcopy(board)
				testBoard.place(x,y, _WHITE)

				move, tval = maxiMin(testBoard, _BLACK, depth, alpha, beta, level + 1)

				if tval > val:
					val = tval
					bestMove = x,y
				if val >= beta:
					return bestMove, val
				alpha = max(alpha, val)

			return bestMove, val


def maxiMin(board, color, depth, alpha, beta, level = 0, weights = _GREEDY_BALANCED):
	bestMove = None
	if depth == level:
			return None, b.eval(board, color, weights)
	else:
		if color == _BLACK:
			board.bPosMoves = board.allMoves(_BLACK)
			val = 9999999
			for m in range(len(board.bPosMoves)):
				x, y = board.bPosMoves[m]
				testBoard = c.deepcopy(board)
				testBoard.place(x,y, _BLACK)

				move, tval = miniMax(testBoard, _WHITE, depth, alpha, beta, level + 1)

				if tval < val:
					val = tval
					bestMove = x,y
				if val <= alpha:
					return bestMove, val
				beta = min(beta, val)

			return bestMove, val

		else:
			board.wPosMoves = board.allMoves(_WHITE)
			val = 9999999
			for m in range(len(board.wPosMoves)):
				x, y = board.wPosMoves[m]
				testBoard = c.deepcopy(board)
				testBoard.place(x,y, _WHITE)

				move, tval = miniMax(testBoard, _BLACK, depth, alpha, beta, level + 1)

				if tval < val:
					val = tval
					bestMove = x,y
				if val <= alpha:
					return bestMove, val
				beta = min(beta, val)

			return bestMove, val

def makeMove(board, color, weights = _AB_DEFAULT):
	if color == _BLACK:
		board.bPosMoves = board.allMoves(_BLACK)
		numMoves = len(board.bPosMoves)

		if numMoves == 0:
			return

		else:
			try:
				(x,y),val = maxiMin(board, _BLACK, _ALPHA_BETA_SEARCH_DEPTH, -9999999, 9999999)
				board.place(x,y, _BLACK)
				return
			except TypeError:
				b.makeMove(board, color, weights)
				return
			

	else:
		board.wPosMoves = board.allMoves(_WHITE)
		numMoves = len(board.wPosMoves)

		if numMoves == 0:
			return

		else:
			try:
				(x,y), val = maxiMin(board, _WHITE, _ALPHA_BETA_SEARCH_DEPTH, -9999999, 9999999)
				board.place(x,y, _WHITE)
				return
			except TypeError:
				b.makeMove(board, color, weights)
				return
			

