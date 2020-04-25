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


def iterateBoard(board):
    newBoard = board.copy()

    for y in range(board.h):
        for x in range(board.w):
            state = board.get(x, y)
            if state == "veg":
                bs = board.neighbors(x, y).count("fire") * IGNITE_PROB
                if bs > random.random():
                    newBoard.set(x, y, "fire")
            elif state == "fire":
                if BURNT_PROB > random.random():
                    newBoard.set(x, y, "burnt")

    return newBoard


board = automata(iterate=iterateBoard, default_state="empty")
board.newState("veg", VEG_FG, VEG_BG, VEG_CHAR, VEG_DENSITY)
board.newState("fire", FIRE_FG, FIRE_BG, FIRE_CHAR, FIRE_DENSITY)
board.newState("burnt", BURNT_FG, BURNT_BG, BURNT_CHAR, 0)
board.newState("empty", EMPTY_FG, EMPTY_BG, EMPTY_CHAR, 0)
board.run()
