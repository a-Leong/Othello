"""
BASIC AI MODULE

BJORNSSON & LEONG PRESENT: IN THE MOOD FOR LOVE: A GAME
CS4701 2017sp


-Citations-

eval(board, color) 
	based on the dynamic heuristic function
	written by Kartik Kukreja:

	< https://github.com/kartikkukreja/blog-codes/blob/master/
	src/Heuristic%20Function%20for%20Reversi%20(Othello).cpp >

"""


import state as s
import random as r
import copy as c


_BLACK = " X"
_WHITE = " 0"
_EMPTY = "  "


# weights : cornerAdjacency, points, corners, mobility, frontier, stability
_GREEDY_DEFAULT = [382.0, 10.0, 801.0, 79.0, 75.0, 10.0]
_GREEDY_AGGRO =  [549.0, 33.0, 625.0, 103.0, 145.0, 75.0]
_GREEDY_BALANCED = [258.9, 0, 595.6, 66.1, 43.8, 17.0]

sMatrix	  = [[20, -3, 11, 8, 8, 11, -3, 20],
			 [-3, -7, -4, 1, 1, -4, -7, -3],
			 [11, -4, 2, 2, 2, 2, -4, 11],
			 [8, 1, 2, -3, -3, 2, 1, 8],
			 [8, 1, 2, -3, -3, 2, 1, 8],
			 [11, -4, 2, 2, 2, 2, -4, 11],
			 [-3, -7, -4, 1, 1, -4, -7, -3],
			 [20, -3, 11, 8, 8, 11, -3, 20]]

xMove = [-1, -1, 0, 1, 1, 1, 0, -1]
yMove = [0, 1, 1, 1, 0, -1, -1, -1];


def mutate(weights):
	a = r.gauss(0, 300) + (r.uniform(0.50, 1.50) * weights[0])
	b = r.gauss(0, 300) + (r.uniform(0.50, 1.50) * weights[1])
	c = r.gauss(0, 300) + (r.uniform(0.50, 1.50) * weights[2])
	d = r.gauss(0, 300) + (r.uniform(0.50, 1.50) * weights[3])
	e = r.gauss(0, 300) + (r.uniform(0.50, 1.50) * weights[4])
	f = r.gauss(0, 300) + (r.uniform(0.50, 1.50) * weights[5])

	mutant = [a,b,c,d,e,f]

	for w in range(6):
		if mutant[w] < 0:
			mutant[w] = 0

	return mutant

# returns a float value associated with [board] if [color] takes the next move
def eval(board, color, weights):
	mobility = 0; stability = 0; frontier = 0; parity = 0; points = 0; corners = 0
	colorTiles = 0; opTiles = 0; emptyTiles = 0; colorFront = 0; opFront = 0

	op = s.opponent(color)

	colorMoves = len(board.allMoves(color))
	opMoves = len(board.allMoves(op))

	# mobility value
	if colorMoves > opMoves:
		mobility = (100.0 * colorMoves) / (colorMoves + opMoves)
	elif colorMoves < opMoves:
		mobility = -(100.0 * opMoves) / (colorMoves + opMoves)

	# stability value / frontier / piece difference
	for i in range(8):
		for j in range(8):
			if board.squares[i][j].tile == color:
				stability += sMatrix[i][j]
				colorTiles += 1

			elif board.squares[i][j].tile == op:
				stability -= sMatrix[i][j]
				opTiles += 1

			else:
				emptyTiles += 1

			if board.squares[i][j].tile != _EMPTY:
				for k in range(8):
					x = i + xMove[k]
					y = j + yMove[k]
					if (x >= 0 and x < 8 and y >= 0 and y < 8 and
						board.squares[x][y].tile == _EMPTY):

						if board.squares[x][y].tile == color:
							colorFront += 1
						else:
							opFront += 1
						break

	if colorTiles > opTiles:
		points = (100.0 * colorTiles) / (colorTiles + opTiles)
	elif colorTiles < opTiles:
		points = -(100.0 * opTiles) / (colorTiles + opTiles)

	if colorFront > opFront:
		frontier = -(100.0 * colorFront) / (colorFront + opFront)
	elif colorFront < opFront:
		frontier = (100.0 * opFront) / (colorFront + opFront)

	# corners
	colorTiles = 0; opTiles = 0
	if board.squares[0][0].tile == color:
		colorTiles += 1
	elif board.squares[0][0].tile == op:
		opTiles += 1
	if board.squares[0][7].tile == color:
		colorTiles += 1
	elif board.squares[0][7].tile == op:
		opTiles += 1
	if board.squares[7][0].tile == color:
		colorTiles += 1
	elif board.squares[7][0].tile == op:
		opTiles += 1
	if board.squares[7][7].tile == color:
		colorTiles += 1
	elif board.squares[7][7].tile == op:
		opTiles += 1

	corners = 25 * (colorTiles - opTiles)

	# corner closeness
	colorTiles = 0; opTiles = 0
	if board.squares[0][0].tile == _EMPTY:
		if board.squares[0][1].tile == color:
			colorTiles += 1
		elif board.squares[0][1].tile == op:
			opTiles += 1
		if board.squares[1][1].tile == color:
			colorTiles += 1
		elif board.squares[1][1].tile == op:
			opTiles += 1
		if board.squares[1][0].tile == color:
			colorTiles += 1
		elif board.squares[1][0].tile == op:
			opTiles += 1

	if board.squares[0][7].tile == _EMPTY:
		if board.squares[0][6].tile == color:
			colorTiles += 1
		elif board.squares[0][6].tile == op:
			opTiles += 1
		if board.squares[1][6].tile == color:
			colorTiles += 1
		elif board.squares[1][6].tile == op:
			opTiles += 1
		if board.squares[1][7].tile == color:
			colorTiles += 1
		elif board.squares[1][7].tile == op:
			opTiles += 1

	if board.squares[7][0].tile == _EMPTY:
		if board.squares[7][1].tile == color:
			colorTiles += 1
		elif board.squares[7][1].tile == op:
			opTiles += 1
		if board.squares[6][1].tile == color:
			colorTiles += 1
		elif board.squares[6][1].tile == op:
			opTiles += 1
		if board.squares[6][0].tile == color:
			colorTiles += 1
		elif board.squares[6][0].tile == op:
			opTiles += 1

	if board.squares[7][7].tile == _EMPTY:
		if board.squares[6][7].tile == color:
			colorTiles += 1
		elif board.squares[6][7].tile == op:
			opTiles += 1
		if board.squares[6][6].tile == color:
			colorTiles += 1
		elif board.squares[6][6].tile == op:
			opTiles += 1
		if board.squares[7][6].tile == color:
			colorTiles += 1
		elif board.squares[7][6].tile == op:
			opTiles += 1

	cornerAdjacency = -12.5 * (colorTiles - opTiles)
	
	return ((weights[0] * cornerAdjacency) + (weights[1] * points) + 
			(weights[2] * corners) + (weights[3] * mobility) + 
			(weights[4] * frontier) + (weights[5] * stability))



def makeMove(board, color, weights):
	if color == _BLACK:
		board.bPosMoves = board.allMoves(_BLACK)
		numMoves = len(board.bPosMoves)

		if numMoves == 0:
			return

		else:
			bestScore = 9999999
			moveID = 0
			for m in range(len(board.bPosMoves)):
				x, y = board.bPosMoves[m]
				testBoard = c.deepcopy(board)
				testBoard.place(x,y, _BLACK)
				moveScore = eval(testBoard, _WHITE, weights)
				if moveScore < bestScore:
					bestScore = moveScore
					moveID = m
			x, y = board.bPosMoves[moveID]
			board.place(x, y, _BLACK)
			return

	else:
		board.wPosMoves = board.allMoves(_WHITE)
		numMoves = len(board.wPosMoves)

		if numMoves == 0:
			return

		else:
			bestScore = 9999999
			moveID = 0

			for m in range(len(board.wPosMoves)):
				x, y = board.wPosMoves[m]
				testBoard = c.deepcopy(board)
				testBoard.place(x,y, _WHITE)
				moveScore = eval(testBoard, _BLACK, weights)
				if moveScore < bestScore:
					bestScore = moveScore
					moveID = m

			x, y = board.wPosMoves[moveID]
			board.place(x, y, _WHITE)
			return
