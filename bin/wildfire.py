#!/usr/bin/python3

import random
from automata import automata

# Stochastic wildland fire spread dynamics
# https://iopscience.iop.org/article/10.1088/1742-6596/285/1/012038/pdf

# ################ CONFIG #################

FIRE_DENSITY = 0.005  # INITIAL AMOUNT OF FIRE
VEG_DENSITY = 0.95    # D
BURNT_PROB = 0.10     # B
IGNITE_PROB = 0.15    # I


VEG_CHAR = ' '
VEG_FG = 0
VEG_BG = 2

FIRE_CHAR = '^'
FIRE_FG = 52
FIRE_BG = 9

BURNT_CHAR = 'x'
BURNT_FG = 0
BURNT_BG = 52

EMPTY_CHAR = ' '
EMPTY_FG = 0
EMPTY_BG = 0

# ################ CONFIG #################


def fireScore(board, x, y):
    n = 0.0

    minx = max(0, x-1)
    maxx = min(board.w-1, x+1)
    miny = max(0, y-1)
    maxy = min(board.h-1, y+1)

    for y2 in range(miny, maxy+1):
        for x2 in range(minx, maxx+1):
            if board.get(x2, y2) == "fire":
                n += IGNITE_PROB
    return n


def iterateBoard(board):
    newBoard = board.copy()

    for y in range(board.h):
        for x in range(board.w):
            if board.get(x, y) == "veg":
                bs = fireScore(board, x, y)
                if bs > random.random():
                    newBoard.set(x, y, "fire")
            elif board.get(x, y) == "fire":
                if BURNT_PROB > random.random():
                    newBoard.set(x, y, "burnt")

    return newBoard


board = automata(iterate=iterateBoard, default_state="empty")
board.newState("veg", VEG_FG, VEG_BG, VEG_CHAR, VEG_DENSITY)
board.newState("fire", FIRE_FG, FIRE_BG, FIRE_CHAR, FIRE_DENSITY)
board.newState("burnt", BURNT_FG, BURNT_BG, BURNT_CHAR, 0)
board.newState("empty", EMPTY_FG, EMPTY_BG, EMPTY_CHAR, 0)
board.run()
