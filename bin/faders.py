#!/usr/bin/env python3

from automata import automata

# https://www.fourmilab.ch/cellab/manual/rules.html#Faders

# ################ CONFIG #################

PARAMS = (127, 2, 2, 2, 2)

# ################ CONFIG #################

N = PARAMS[0]
L = PARAMS[1]
U = PARAMS[2]
K = PARAMS[3]
Y = PARAMS[4]


def new_state(board, x, y):
    oldstate = board.get(x, y)
    sum_8 = sum(board.neighbors(x, y))
    n = 0

    if (oldstate == 0) and (L <= sum_8) and (sum_8 <= U):
        n = 1

    if (oldstate == 1):
        if (K <= sum_8) and (sum_8 <= Y):
            n = 1
        else:
            n = 2

    if ((oldstate & 1) == 0) and (0 < oldstate) and (oldstate < (2*N)):
        n = oldstate + 2
    return n


def iterate_board(board):
    board.wrap = True
    newBoard = board.new()

    for y in range(board.h):
        for x in range(board.w):
            newBoard.set(x, y, new_state(board, x, y))

    return newBoard


a = automata(iterate=iterate_board, default_state=0)

for i in range(0, (N*2)+1):
    a.new_state(i, i, i, ' ', .001)

a.run()
