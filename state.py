"""
GAMESTATE MODULE

Author: Alex Leong
"""


import string
import copy as c


_BLACK = " X"
_WHITE = " 0"
_EMPTY = "  "
_TIE = " 0"


class GetHelp(Exception):
    pass

class InvalidInput(Exception):
    pass

class InvalidMove(Exception):
    pass

class Quit(Exception):
    pass

class Square(object):
    def __init__(self, tile):
        self.tile = tile

class Board(object):
    def __init__(self):
        self.squares = [[Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY),
                         Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY)],
                        [Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY),
                         Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY)],
                        [Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY),
                         Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY)],
                        [Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_WHITE),
                         Square(_BLACK), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY)],
                        [Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_BLACK),
                         Square(_WHITE), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY)],
                        [Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY),
                         Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY)],
                        [Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY),
                         Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY)],
                        [Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY),
                         Square(_EMPTY), Square(_EMPTY), Square(_EMPTY), Square(_EMPTY)]]
        self.blackTileCT = 2
        self.whiteTileCT = 2
        self.bPosMoves = self.allMoves(_BLACK)
        self.wPosMoves = self.allMoves(_WHITE)
        self.winner = ""

    # returns the list of all squares taken by [color] from [color]'s opponent if
    # if a [color] tile is played at [x],[y]. if an empty list is returned, the move
    # is invalid.
    def flanks(self, x1, y1, color):

        # returns a list of the squares which contain [color]'s opponent's tiles
        # between the orignial square at [x1],[y1] and the square at [x],[y].
        # recurses unidirectionally.
        def recurse(board, x, y, prevX, prevY, color, acc):
            if x < 0 or x > 7 or y < 0 or y > 7:
                return []

            elif board.squares[x][y].tile == _EMPTY:
                return []

            elif board.squares[x][y].tile == color:
                return acc

            else:
                newX = x + x - prevX
                newY = y + y - prevY
                acc.append(board.squares[x][y])
                return recurse(board, newX, newY, x, y, color, acc)

        squaresTaken = []

        for i in range (-1, 2):
            for j in range (-1, 2):
                
                squaresTaken.extend(recurse(self, x1 + i, y1 + j, x1, y1, color, []))

        return squaresTaken

    # places a tile of color [color] at square [x],[y] and flips all flanked tiles
    # if move is legal. raises exception otherwise.
    def place(self, x, y, color):
        if self.squares[x][y].tile == _EMPTY:
            taken = self.flanks(x, y, color)
            numTaken = len(taken)
            if numTaken > 0:
                for s in taken:
                    s.tile = color
                self.squares[x][y].tile = color
                self.updateScore(color, numTaken)

            else:
                raise InvalidMove("must flank an oppenent's tile")

        else:
            raise InvalidMove("must place tile in empty square")


    # returns a list of all possible moves where an element of the list
    # is a tuple (x,y)
    def allMoves(self, color):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.squares[i][j].tile == _EMPTY:
                    if self.flanks(i,j,color) != []:
                        moves.append((i,j))
        return moves

    def allNextStates(self, color):
        states = []
        moves = self.allMoves(color)

        for m in moves:
            x, y = m
            iBoard = c.deepcopy(self)
            iBoard.place(x,y, color)

            states.append(iBoard)

        return states

    # iterates through every square updating players' tile counts.
    def updateScore(self, color, newTiles):
        if color == _BLACK:
            self.blackTileCT += newTiles + 1
            self.whiteTileCT -= newTiles
        else:
            self.blackTileCT -= newTiles
            self.whiteTileCT += newTiles + 1

    # prints the board.
    def printer(self):
        boardGraphic = """
             a   b   c   d   e   f   g   h
          -----------------------------------
        1 | %s  %s  %s  %s  %s  %s  %s  %s  | 1
          |                                 |
        2 | %s  %s  %s  %s  %s  %s  %s  %s  | 2
          |                                 |
        3 | %s  %s  %s  %s  %s  %s  %s  %s  | 3
          |                                 |
        4 | %s  %s  %s  %s  %s  %s  %s  %s  | 4
          |                                 |
        5 | %s  %s  %s  %s  %s  %s  %s  %s  | 5
          |                                 |
        6 | %s  %s  %s  %s  %s  %s  %s  %s  | 6
          |                                 |
        7 | %s  %s  %s  %s  %s  %s  %s  %s  | 7
          |                                 |
        8 | %s  %s  %s  %s  %s  %s  %s  %s  | 8
          ----------------------------------- 
             a   b   c   d   e   f   g   h

             Black(X): %s pts    White(0): %s pts

         """ % (self.squares[0][0].tile, 
        self.squares[0][1].tile, self.squares[0][2].tile, 
        self.squares[0][3].tile, self.squares[0][4].tile, self.squares[0][5].tile, 
        self.squares[0][6].tile, self.squares[0][7].tile, self.squares[1][0].tile, 
        self.squares[1][1].tile, self.squares[1][2].tile, self.squares[1][3].tile, 
        self.squares[1][4].tile, self.squares[1][5].tile, self.squares[1][6].tile, 
        self.squares[1][7].tile, self.squares[2][0].tile, self.squares[2][1].tile, 
        self.squares[2][2].tile, self.squares[2][3].tile, self.squares[2][4].tile, 
        self.squares[2][5].tile, self.squares[2][6].tile, self.squares[2][7].tile, 
        self.squares[3][0].tile, self.squares[3][1].tile, self.squares[3][2].tile, 
        self.squares[3][3].tile, self.squares[3][4].tile, self.squares[3][5].tile, 
        self.squares[3][6].tile, self.squares[3][7].tile, self.squares[4][0].tile, 
        self.squares[4][1].tile, self.squares[4][2].tile, self.squares[4][3].tile, 
        self.squares[4][4].tile, self.squares[4][5].tile, self.squares[4][6].tile, 
        self.squares[4][7].tile, self.squares[5][0].tile, self.squares[5][1].tile, 
        self.squares[5][2].tile, self.squares[5][3].tile, self.squares[5][4].tile, 
        self.squares[5][5].tile, self.squares[5][6].tile, self.squares[5][7].tile, 
        self.squares[6][0].tile, self.squares[6][1].tile, self.squares[6][2].tile, 
        self.squares[6][3].tile, self.squares[6][4].tile, self.squares[6][5].tile, 
        self.squares[6][6].tile, self.squares[6][7].tile, self.squares[7][0].tile, 
        self.squares[7][1].tile, self.squares[7][2].tile, self.squares[7][3].tile, 
        self.squares[7][4].tile, self.squares[7][5].tile, self.squares[7][6].tile, 
        self.squares[7][7].tile, self.blackTileCT, self.whiteTileCT)

        print boardGraphic

def update(board, toMove, inGame):
    if board.bPosMoves == [] and board.wPosMoves == []:
        if board.whiteTileCT > board.blackTileCT:
            board.winner = _WHITE
            inGame = False
            return inGame, toMove

        elif board.blackTileCT > board.whiteTileCT:
            board.winner = _BLACK
            inGame = False
            return inGame, toMove

        else:
            board.winner = _TIE
            inGame = False
            return inGame, toMove

    if toMove == _BLACK:
        toMove = _WHITE

    elif toMove == _WHITE:
        toMove = _BLACK

    return inGame, toMove

# returns the opponent of [color]
def opponent(color):
    if color == _BLACK:
        return _WHITE
    elif color == _WHITE:
        return _BLACK
    else:
        raise InvalidInput

# returns a tuple of x,y indices for valid input, raises exception otherwise.
def parse(_input):
    xValues = "12345678"
    yValues = "abcdefgh"

    _input = str(_input)

    if _input == "quit" or _input == "q" or _input == "exit":
        raise Quit

    elif _input == "help" or _input == "hint":
        raise GetHelp

    elif (len(_input) != 2) or (_input[0] not in yValues) or (_input[1] not in xValues):
        raise ValueError("invalid input: " + _input)

    else:
        x = xValues.index(_input[1])
        y = yValues.index(_input[0])

        return x, y


# reads for input and makes move if possible, tries again otherwise.
# returns false when input is a quit command, true otherwise.
def makeMove(board, toMove):
    while True:
        if toMove == _BLACK:
            board.bPosMoves = board.allMoves(_BLACK)
            if board.bPosMoves == []:
                print "No possible moves for black"
                return True
            print "black to move"

        else:
            board.wPosMoves = board.allMoves(_WHITE)
            if board.wPosMoves == []:
                print "No possible moves for white"
                return True
            print "white to move"

        try:
            _in = raw_input("> ")
            x, y = parse(_in)

            board.place(x,y, toMove)

            return True

        except ValueError as err:
            board.printer()
            print err.args[0]

        except InvalidMove as err:
            board.printer()
            print err.args[0]

        except GetHelp:
            board.printer()
            if toMove == _BLACK:
                print "Possible moves: ", board.bPosMoves
            else:
                print "Possible moves: ", board.wPosMoves

        except Quit:
            return False
