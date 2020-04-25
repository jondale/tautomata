#!/usr/bin/python3

from automata import automata

# Conway's game of life

# ################ CONFIG #################

CHANCE_OF_LIFE = .15

LIVE_CHAR = ' '
LIVE_FG = 254
LIVE_BG = 45
DEAD_CHAR = ' '
DEAD_FG = 233
DEAD_BG = 16

# ################ CONFIG #################


def numNeighbors(board, x, y):
    n = 0

    minx = max(0, x-1)
    maxx = min(board.w-1, x+1)
    miny = max(0, y-1)
    maxy = min(board.h-1, y+1)

    for y2 in range(miny, maxy+1):
        for x2 in range(minx, maxx+1):
            if (x2 != x or y2 != y) and board.get(x2, y2) == "live":
                n += 1
    return n


def iterateBoard(board):
    newBoard = board.new()

    for y in range(board.h):
        for x in range(board.w):
            n = numNeighbors(board, x, y)
            if board.get(x, y) == "live" and n in (2, 3):
                newBoard.set(x, y, "live")
            elif n == 3:
                newBoard.set(x, y, "live")
    return newBoard


life = automata(iterate=iterateBoard, default_state="dead")
life.newState("live", LIVE_FG, LIVE_BG, LIVE_CHAR, CHANCE_OF_LIFE)
life.newState("dead", DEAD_FG, DEAD_BG, DEAD_CHAR, 0)
life.run()
