#!/usr/bin/python3

from automata import automata

# https://en.wikipedia.org/wiki/Brian's_Brain

# ################ CONFIG #################

# How dense to orinally populate the board.
# .25 seems to give best results
CHANCE_OF_LIFE = .25

WRAP_BOARD = True

LIVE_CHAR = ' '
LIVE_FG = 254
LIVE_BG = 45
DYING_CHAR = ' '
DYING_FG = 0
DYING_BG = 20
DEAD_CHAR = ' '
DEAD_FG = 233
DEAD_BG = 16

# ################ CONFIG #################


def numNeighbors(board, x, y):
    n = 0

    minx = x-1
    maxx = x+1
    miny = y-1
    maxy = y+1

    for y2 in range(miny, maxy+1):
        for x2 in range(minx, maxx+1):
            val = board.get(x2, y2, wrap=WRAP_BOARD)
            if (x2 != x or y2 != y) and val == "live":
                n += 1
    return n


def iterateLife(board):
    newBoard = board.new()
    for y in range(board.h):
        for x in range(board.w):
            n = numNeighbors(board, x, y)
            state = board.get(x, y)
            if state == "live":
                newBoard.set(x, y, "dying")
            elif state == "dying":
                newBoard.set(x, y, "dead")
            elif state == "dead" and n == 2:
                newBoard.set(x, y, "live")
    return newBoard.copy()


a = automata(iterate=iterateLife, default_state="dead")
a.newState("live", LIVE_FG, LIVE_BG, LIVE_CHAR, CHANCE_OF_LIFE)
a.newState("dying", DYING_FG, DYING_BG, DYING_CHAR, 0)
a.newState("dead", DEAD_FG, DEAD_BG, DEAD_CHAR, 0)
a.run()
