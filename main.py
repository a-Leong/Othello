"""
MAIN MODULE

BJORNSSON & LEONG PRESENT: IN THE MOOD FOR LOVE: A GAME
CS4701 2017sp
"""

import state as s
import randAI as rand
import basicAI as base
import alphaBeta as ab
import string
import sys
import time
from multiprocessing import Pool


_BLACK = " X"
_WHITE = " 0"
_EMPTY = "  "
_TIE = " 0"

_RUNS_PER_PROCESS_LOW = 4
_RUNS_PER_PROCESS_HIGH = 2500
_PROCESSES = 4              # no performance benefit to increase beyond # cores

def readable(color):
    if color == _BLACK:
        return "black"
    elif color == _WHITE:
        return "white"
    else:
        return "neither color"


##############################################################################
##############################################################################
#                        REPLs for human players
##############################################################################
##############################################################################
def twoPlayerREPL():
    try:
        print "\n           ===== Welcome to Othello =====\n"
        print "                  input example: b4\n"
        print "                      q to quit\n"
        print "               * Press Enter to Start *"

        # setup game
        mainBoard = s.Board()
        toMove = _BLACK
        inGame = True

        raw_input("")

        # make moves
        while inGame:  

            mainBoard.printer()

            inGame = s.makeMove(mainBoard, toMove)

            inGame, toMove = s.update(mainBoard, toMove, inGame)

    except KeyboardInterrupt:
        pass

    print readable(mainBoard.winner), "wins"
    print "\n\ngoodbye \n"


def onePlayerREPL():
    try:
        print "\n           ===== Welcome to Othello =====\n"
        print "                  input example: b4\n"
        print "                      q to quit\n"

        # setup game
        mainBoard = s.Board()
        toMove = _BLACK
        inGame = True

        # player choose color
        while True:
            try:
                _in = raw_input("which color would you like to play? (b/w)\n> ")
                if _in == 'b':
                    playerColor = _BLACK
                    aiColor = _WHITE
                    break
                elif _in == 'w':
                    playerColor = _WHITE
                    aiColor = _BLACK
                    break

            except:
                print "invalid input"

        # player choose opponent
        while True:
            try:
                _in = raw_input("against which AI would you like to play? (normal/hard)\n> ")
                if _in == 'normal':
                    aiType = "base"
                    break
                elif _in == 'hard':
                    aiType = "ab"
                    break

            except:
                print "invalid input"

        # make moves
        while inGame:  

            mainBoard.printer()

            if playerColor == toMove:
                inGame = s.makeMove(mainBoard, playerColor)

            else:
                time.sleep(0.8)
                if aiType == "base":
                    base.makeMove(mainBoard, aiColor, base._GREEDY_BALANCED)
                else:
                    ab.makeMove(mainBoard, aiColor, ab._AB_DEFAULT)

            inGame, toMove = s.update(mainBoard, toMove, inGame)

    except KeyboardInterrupt:
        pass

    print readable(mainBoard.winner), "wins"
    print "\n\ngoodbye \n"


##############################################################################
##############################################################################
#                        one game AI vs AI functions
##############################################################################
##############################################################################

def randVSrand(isStatRun):

    mainBoard = s.Board()
    inGame = True
    toMove = _BLACK

    bMoves = 0.0
    wMoves = 0.0
    wBranch = 0.0
    bBranch = 0.0

    while inGame:
        mainBoard.printer()             # uncomment to watch entire game
        time.sleep(0.4)                 #

        # collect branch factor data to pass to stats functions
        if toMove == _BLACK:
            bMoves += 1
            bBranch += len(mainBoard.bPosMoves)
        else:
            wMoves += 1
            wBranch += len(mainBoard.wPosMoves)

        rand.makeMove(mainBoard, toMove)

        inGame, toMove = s.update(mainBoard, toMove, inGame)

    if isStatRun:
        return mainBoard, wBranch/wMoves, bBranch/bMoves

    else:
        mainBoard.printer()
        print readable(mainBoard.winner), "wins"


def randVSab(isStatRun, _type):

    mainBoard = s.Board()
    inGame = True
    toMove = _BLACK

    bMoves = 0.0
    rMoves = 0.0
    rBranch = 0.0
    bBranch = 0.0
    greedyWin = 0
    randWin = 0

    while inGame:
        mainBoard.printer()             # uncomment to watch entire game
        time.sleep(0.4)                 #

        # collect branch factor data to pass to stats functions
        if _type % 2 == 1:
            if toMove == _BLACK:
                rMoves += 1
                rBranch += len(mainBoard.bPosMoves)
                base.makeMove(mainBoard, toMove, base._GREEDY_BALANCED)

            else:
                bMoves += 1
                bBranch += len(mainBoard.wPosMoves)
                ab.makeMove(mainBoard, toMove, ab._AB_DEFAULT)

        else:

            if toMove == _WHITE:
                rMoves += 1
                rBranch += len(mainBoard.wPosMoves)
                base.makeMove(mainBoard, toMove, base._GREEDY_BALANCED)

            else:
                
                bMoves += 1
                bBranch += len(mainBoard.bPosMoves)
                ab.makeMove(mainBoard, toMove, ab._AB_DEFAULT)
                
        inGame, toMove = s.update(mainBoard, toMove, inGame)
        
    if _type % 2 == 1 and mainBoard.winner == _WHITE:
        greedyWin = 1
    elif _type % 2 == 0 and mainBoard.winner == _BLACK:
        greedyWin = 1
    else:
        randWin = 1


    if isStatRun:
        return mainBoard, rBranch/rMoves, bBranch/bMoves, greedyWin, randWin

    else:
        mainBoard.printer()
        print readable(mainBoard.winner), "wins"


def baseVSbase(isStatRun, w1 = base._GREEDY_BALANCED, w2 = base._GREEDY_BALANCED):

    mainBoard = s.Board()
    inGame = True
    toMove = _BLACK

    bMoves = 0.0
    wMoves = 0.0
    wBranch = 0.0
    bBranch = 0.0

    while inGame:
        mainBoard.printer()             # uncomment to watch entire game
        time.sleep(0.4)                 #

        # collect branch factor data to pass to stats functions
        if toMove == _BLACK:
            bMoves += 1
            bBranch += len(mainBoard.bPosMoves)
            base.makeMove(mainBoard, toMove, w1)

        else:
            wMoves += 1
            wBranch += len(mainBoard.wPosMoves)
            base.makeMove(mainBoard, toMove, w2)

        inGame, toMove = s.update(mainBoard, toMove, inGame)

    if isStatRun:

        bWin = 0
        wWin = 0
        tie = 0

        margin = (mainBoard.blackTileCT - mainBoard.whiteTileCT)

        if mainBoard.winner == _BLACK:
            bWin = 1
            winnerW = w1
        elif mainBoard.winner == _WHITE:
            wWin = 1
            winnerW = w2
        else:
            tie = 1
            winnerW = []

        return [bWin, wWin, tie, bBranch/bMoves, wBranch/wMoves, margin, winnerW]

    else:
        mainBoard.printer()
        print readable(mainBoard.winner), "wins"



def abVSab(isStatRun, _type = 0, w1 = base._GREEDY_BALANCED, w2 = base._GREEDY_BALANCED):

    mainBoard = s.Board()
    inGame = True
    toMove = _BLACK

    bMoves = 0.0
    wMoves = 0.0
    wBranch = 0.0
    bBranch = 0.0

    while inGame:
        mainBoard.printer()                # uncomment to watch entire game
        #time.sleep(0.4)                    #

        # collect branch factor data to pass to stats functions
        if _type % 2 == 1:
            if toMove == _BLACK:
                bMoves += 1
                bBranch += len(mainBoard.bPosMoves)
                ab.makeMove(mainBoard, toMove, w1)

            else:
                wMoves += 1
                wBranch += len(mainBoard.wPosMoves)
                base.makeMove(mainBoard, toMove, w2)

        else:
            if toMove == _WHITE:
                wMoves += 1
                wBranch += len(mainBoard.wPosMoves)
                ab.makeMove(mainBoard, toMove, w2)

            else:
                bMoves += 1
                bBranch += len(mainBoard.bPosMoves)
                base.makeMove(mainBoard, toMove, w1)

        inGame, toMove = s.update(mainBoard, toMove, inGame)


    if isStatRun:
        bWin = 0
        wWin = 0
        tie = 0

        margin = (mainBoard.blackTileCT - mainBoard.whiteTileCT)

        if mainBoard.winner == _BLACK:
            bWin = 1
            winnerW = w1
        elif mainBoard.winner == _WHITE:
            wWin = 1
            winnerW = w2
        else:
            tie = 1
            winnerW = []

        return [bWin, wWin, tie, bBranch/bMoves, wBranch/wMoves, margin, winnerW]

    else:
        mainBoard.printer()
        print readable(mainBoard.winner), "wins"


def abVSab(isStatRun, _type = 0, w1 = base._GREEDY_BALANCED, w2 = base._GREEDY_BALANCED):

    mainBoard = s.Board()
    inGame = True
    toMove = _BLACK

    bMoves = 0.0
    wMoves = 0.0
    wBranch = 0.0
    bBranch = 0.0

    while inGame:
        mainBoard.printer()                # uncomment to watch entire game
        time.sleep(3)                      #

        # collect branch factor data to pass to stats functions
        if _type % 2 == 1:
            if toMove == _BLACK:
                bMoves += 1
                bBranch += len(mainBoard.bPosMoves)
                ab.makeMove(mainBoard, toMove, w1)

            else:
                wMoves += 1
                wBranch += len(mainBoard.wPosMoves)
                ab.makeMove(mainBoard, toMove, w2)

        else:
            if toMove == _WHITE:
                wMoves += 1
                wBranch += len(mainBoard.wPosMoves)
                ab.makeMove(mainBoard, toMove, w2)

            else:
                bMoves += 1
                bBranch += len(mainBoard.bPosMoves)
                ab.makeMove(mainBoard, toMove, w1)

        inGame, toMove = s.update(mainBoard, toMove, inGame)


    if isStatRun:
        bWin = 0
        wWin = 0
        tie = 0

        margin = (mainBoard.blackTileCT - mainBoard.whiteTileCT)

        if mainBoard.winner == _BLACK:
            bWin = 1
            winnerW = w1
        elif mainBoard.winner == _WHITE:
            wWin = 1
            winnerW = w2
        else:
            tie = 1
            winnerW = []

        return [bWin, wWin, tie, bBranch/bMoves, wBranch/wMoves, margin, winnerW]

    else:
        mainBoard.printer()
        print readable(mainBoard.winner), "wins"

##############################################################################
##############################################################################
#                        AI vs AI functions for stats
##############################################################################
##############################################################################

def randABStats():
    bWin = 0
    wWin = 0
    tie = 0
    rBranch = 0
    bBranch = 0
    margin = 0
    greedyWin = 0 
    randWin = 0

    for i in range(_RUNS_PER_PROCESS_LOW):

        b, rB, bB, gw, rw = randVSab(True, i)

        rBranch += rB
        bBranch += bB
        margin += (b.blackTileCT - b.whiteTileCT)
        greedyWin += gw
        randWin += rw

        sys.stdout.write("\rRunning sim group: %i of " % (i + 1) +
                         str(_RUNS_PER_PROCESS_LOW))
        sys.stdout.flush()

        if b.winner == _BLACK:
            bWin += 1
        elif b.winner == _WHITE:
            wWin += 1
        else:
            tie += 1

    return [bWin, wWin, tie, rBranch, bBranch, margin, greedyWin, randWin]


def abBaseStats():
    bWin = 0
    wWin = 0
    tie = 0
    rBranch = 0
    bBranch = 0
    margin = 0
    greedyWin = 0 
    randWin = 0

    for i in range(_RUNS_PER_PROCESS_LOW):

        b, rB, bB, gw, rw = abVSab(True, i)

        rBranch += rB
        bBranch += bB
        margin += (b.blackTileCT - b.whiteTileCT)
        greedyWin += gw
        randWin += rw

        sys.stdout.write("\rRunning sim group: %i of " % (i + 1) +
                         str(_RUNS_PER_PROCESS_LOW))
        sys.stdout.flush()

        if b.winner == _BLACK:
            bWin += 1
        elif b.winner == _WHITE:
            wWin += 1
        else:
            tie += 1

    return [bWin, wWin, tie, rBranch, bBranch, margin, greedyWin, randWin]

def randStats():
    bWin = 0
    wWin = 0
    tie = 0
    wBranch = 0
    bBranch = 0
    margin = 0

    for i in range(_RUNS_PER_PROCESS_HIGH):

        b, wB, bB = randVSrand(True)

        wBranch += wB
        bBranch += bB
        margin += (b.blackTileCT - b.whiteTileCT)

        sys.stdout.write("\rRunning sim group: %i of " % (i + 1) +
                         str(_RUNS_PER_PROCESS_HIGH))
        sys.stdout.flush()

        if b.winner == _BLACK:
            bWin += 1
        elif b.winner == _WHITE:
            wWin += 1
        else:
            tie += 1

    return [bWin, wWin, tie, wBranch, bBranch, margin, 0, 0]


##############################################################################
##############################################################################
#               multiprocessing function for parallel stats runs
##############################################################################
##############################################################################

# runs _PROCESSES instances of [gameFunction] in parallel
def runParallelTest(gameFunction, nRuns, args = []):

    pool = Pool(_PROCESSES)

    results = []

    for i in range(_PROCESSES):
        pool.apply_async(gameFunction, args, callback = results.append)

    pool.close()    
    pool.join()

    abWin = 0
    bWin = 0
    wWin = 0
    tie = 0
    wBranch = 0
    rBranch = 0
    abBranch = 0
    bBranch = 0
    margin = 0
    greedyWin = 0
    randWin = 0
    abWin = 0

    if gameFunction == abBaseStats:
        for r in results:
            bWin += r[0]
            wWin += r[1]
            tie += r[2]
            abBranch += r[4]
            bBranch += r[3]
            margin += r[5]
            greedyWin += r[6]
            abWin += r[7]
    elif gameFunction == randABStats: 
        for r in results:
            bWin += r[0]
            wWin += r[1]
            tie += r[2]
            rBranch += r[4]
            bBranch += r[3]
            margin += r[5]
            greedyWin += r[6]
            randWin += r[7]
    else:
        for r in results:
            bWin += r[0]
            wWin += r[1]
            tie += r[2]
            wBranch += r[4]
            bBranch += r[3]
            margin += r[5]
            greedyWin += r[6]
            randWin += r[7]

    totalRuns = nRuns * _PROCESSES

    print "\n\n===== simulated ", totalRuns, " game(s) ====="
    print "black wins: %", (float(bWin) / totalRuns) * 100
    print "white wins: %", (float(wWin) / totalRuns) * 100
    print "tie:        %", (float(tie) / totalRuns) * 100
    print "avg pt margin blackCt - whiteCt: ", (float(margin) / totalRuns), "pts"
    
    if gameFunction == randABStats:
        print "AB wins: %", (float(greedyWin) / totalRuns) * 100
        print "rand wins: %", (float(randWin) / totalRuns) * 100
        print "avg branching factor for AB: ", bBranch / totalRuns
        print "avg branching factor for rand: ", rBranch / totalRuns, "\n"

    elif gameFunction == abBaseStats:
        print "greedy wins: %", (float(greedyWin) / totalRuns) * 100
        print "alpha beta wins: %", (float(abWin) / totalRuns) * 100
        print "avg branching factor for greedy: ", bBranch / totalRuns
        print "avg branching factor for alpha beta: ", abBranch / totalRuns, "\n"

    else:
        print "avg branching factor for black: ", bBranch / totalRuns
        print "avg branching factor for white: ", wBranch / totalRuns, "\n"

def evolve():
    bestscore = 10
    best_weights = ab._AB_DEFAULT

    showProgress = 0

    try:
        while True:

            showProgress += 1
            pool = Pool(8)

            run1 = []
            run2 = []
            run3 = []
            run4 = []
            run5 = []
            run6 = []
            run7 = []
            run8 = []

            new_weights = base.mutate(base._GREEDY_DEFAULT)
            
            pool.apply_async(abVSab, [True, 0, base._GREEDY_BALANCED, new_weights], callback = run1.append)
            pool.apply_async(abVSab, [True, 1, new_weights, base._GREEDY_BALANCED], callback = run2.append)
            pool.apply_async(abVSab, [True, 0, base._GREEDY_AGGRO, new_weights], callback = run3.append)
            pool.apply_async(abVSab, [True, 1, new_weights, base._GREEDY_AGGRO], callback = run4.append)
            pool.apply_async(abVSab, [True, 0, base._GREEDY_DEFAULT, new_weights], callback = run5.append)
            pool.apply_async(abVSab, [True, 1, new_weights, base._GREEDY_DEFAULT], callback = run6.append)
            pool.apply_async(abVSab, [True, 0, best_weights, new_weights], callback = run7.append)
            pool.apply_async(abVSab, [True, 1, new_weights, best_weights], callback = run8.append)

            pool.close()    
            pool.join()

            if run1[0][1] & run2[0][0] & run3[0][1] & run4[0][0] & run5[0][1] & run6[0][0] & run7[0][1] & run8[0][0]:


                score1 = (((run1[0][4] * 10) - (run1[0][3] * 10) - run1[0][5]) +
                        ((run2[0][3] * 10) - (run2[0][4] * 10) + run2[0][5])) / 2

                score2 = (((run3[0][4] * 10) - (run3[0][3] * 10) - run3[0][5]) +
                        ((run4[0][3] * 10) - (run4[0][4] * 10) + run4[0][5])) / 2

                score3 = (((run5[0][4] * 10) - (run5[0][3] * 10) - run5[0][5]) +
                        ((run6[0][3] * 10) - (run6[0][4] * 10) + run6[0][5])) / 2

                score4 = (((run7[0][4] * 10) - (run7[0][3] * 10) - run7[0][5]) +
                        ((run8[0][3] * 10) - (run8[0][4] * 10) + run8[0][5])) / 2

                scoreAvg = (score1 + score2 + score3 + score4) / 4

                sys.stdout.write("\ragainst balanced: %.2f   " % score1 + "against aggro: %.2f   " % score2 + "against default: %.2f   " % score3 + "against latest: %.2f" % score4 + " "*10)
                sys.stdout.flush()

                if scoreAvg > bestscore:
                    best_weights = new_weights
                    bestscore = scoreAvg
                    print "\nbest weights so far: ", best_weights
                    print "score: ", bestscore

            else:
                sys.stdout.write("\rmutating" + ".."*(showProgress % 10) + " "*(18 - 2*(showProgress % 10)))
                sys.stdout.flush()

    except KeyboardInterrupt:
        pass

    finally:
        print "\n\nbest weights so far: ", best_weights, "\n"


if __name__ == "__main__":

    if len(sys.argv) == 1:
        twoPlayerREPL()
    
    else:
        gameType = str(sys.argv[1])

        if gameType == "ai":
            onePlayerREPL()

        elif gameType == "randvsrand":
            randVSrand(False)

        elif gameType == "randvsab":
            randVSab(False, 1)

        elif gameType == "basevsbase":
            baseVSbase(False)

        elif gameType == "randabstats":
            runParallelTest(randABStats, _RUNS_PER_PROCESS_LOW)

        elif gameType == "randstats":
            runParallelTest(randStats, _RUNS_PER_PROCESS_HIGH)

        elif gameType == "basestats":
            baseVSbase(True)

        elif gameType == "basevsab":
            abVSab(False, 1)

        elif gameType == "abbasestats":
            runParallelTest(abBaseStats, _RUNS_PER_PROCESS_LOW)

        elif gameType == "evolve":
            evolve()

        else:
            print "failure"


