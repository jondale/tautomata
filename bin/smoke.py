#!/usr/bin/env python3

from automata import automata

# ################ CONFIG #################

COLOR_START = 232
NUM_STATES = 22     # These two must have a sum <= 255

CHAR = " "
NEIGHBORHOOD = 1    # How far out to look at neighbors
WRAP = True         # Wrap board?

FADE = 1

# ################ CONFIG #################


def init_board(board):
    new_board = board.copy()
    new_board.set(5, 5, f"{MAXPOWER}.0")
    return new_board


def iterate_board(board):
    board.wrap = WRAP
    new_board = board.new()
    for y in range(board.h):
        for x in range(board.w):
            state = board.get(x, y)
            n = [0 if x is None else x for x in board.neighbors(x, y, NEIGHBORHOOD)]
            newstate = round(max(0, sum(n) / len(n)) - FADE)
            if newstate == 0:
                newstate = NUM_STATES
            new_board.set(x, y, newstate)
    return new_board


a = automata(iterate=iterate_board, default_state=0)
for i in range(NUM_STATES+1):
    a.new_state(i, i+COLOR_START, i+COLOR_START, CHAR, 0.01)
a.run()