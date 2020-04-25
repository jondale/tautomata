#!/usr/bin/python3

from automata import automata

# https://www.emis.de/journals/DMTCS/pdfpapers/dmAA0113.pdf

# Essentially, the game of life where the size of the neighborhood,
# the birth range, and the survival range are definable.

# ################ CONFIG #################

# How dense to orinally populate the board.
# .25 seems to give best results
CHANCE_OF_LIFE = .25

PARAMS = (5, 34, 45, 34, 58)   # paper example #1
# PARAMS = (5, 9, 9, 9, 17)      # paper example #2
# PARAMS = (5, 34, 47, 34, 60)   # paper example #3
# PARAMS = (5, 34, 41, 34, 58)   # paper example #4
# PARAMS = (1, 3, 3, 2, 3)       # Conway's game of life

WRAP_BOARD = True

LIVE_CHAR = ' '
LIVE_FG = 254
LIVE_BG = 45
DEAD_CHAR = ' '
DEAD_FG = 233
DEAD_BG = 16

# ################ CONFIG #################

P = PARAMS[0]    # Neighborhood size
B1 = PARAMS[1]   # Birth range min
B2 = PARAMS[2]   # Birth range max
S1 = PARAMS[3]   # Survive range min
S2 = PARAMS[4]   # Survive range max


def iterateLife(board):
    board.wrap = WRAP_BOARD
    newBoard = board.new()
    for y in range(board.h):
        for x in range(board.w):
            n = board.neighbors(x, y, P).count("live")
            if board.get(x, y) == "live" and n >= S1 and n <= S2:
                newBoard.set(x, y, "live")
            elif n >= B1 and n <= B2:
                newBoard.set(x, y, "live")
    return newBoard.copy()


a = automata(iterate=iterateLife, default_state="dead")
a.newState("live", LIVE_FG, LIVE_BG, LIVE_CHAR, CHANCE_OF_LIFE)
a.newState("dead", DEAD_FG, DEAD_BG, DEAD_CHAR, 0)
a.run()
