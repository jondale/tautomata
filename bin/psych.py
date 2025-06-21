#!/usr/bin/python3

from automata import automata

# ################ CONFIG #################

MAXHEIGHT = 255 
CHAR = " "

# ################ CONFIG #################


def init_board(board):
    new_board = board.copy()
    new_board.set(5, 5, f"{MAXPOWER}.0")
    return new_board


def iterate_board(board):
    board.wrap = True
    new_board = board.new()
    for y in range(board.h):
        for x in range(board.w):
            state = board.get(x, y)
            n = board.neighbors(x, y)
            newstate = round(max(0, (sum(n) + state) / (len(n) + 1) - 1))
            newstate = round(max(0, sum(n) / len(n))) - 1
            if newstate == 0:
                newstate = MAXHEIGHT
            new_board.set(x, y, newstate)
    return new_board


a = automata(iterate=iterate_board, default_state=0)
for i in range(MAXHEIGHT+1):
    a.new_state(i, i, i, CHAR, 0.01)
a.run()