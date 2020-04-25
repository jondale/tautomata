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


def iterateBoard(board):
    newBoard = board.new()

    for y in range(board.h):
        for x in range(board.w):
            n = board.neighbors(x, y).count("live")
            if board.get(x, y) == "live" and n in (2, 3):
                newBoard.set(x, y, "live")
            elif n == 3:
                newBoard.set(x, y, "live")
    return newBoard


life = automata(iterate=iterateBoard, default_state="dead")
life.newState("live", LIVE_FG, LIVE_BG, LIVE_CHAR, CHANCE_OF_LIFE)
life.newState("dead", DEAD_FG, DEAD_BG, DEAD_CHAR, 0)
life.run()
