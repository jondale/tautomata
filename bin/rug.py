#!/usr/bin/python3

from automata import automata

# RUG
# https://www.fourmilab.ch/cellab/manual/rules.html#Rug
#

# ################ CONFIG #################

POP_LEVEL = 100
POP_DENSITY = 0.85
WRAP_BOARD = False

# ################ CONFIG #################


def rugScore(board, x, y):

    sum = 0
    sum += 4 * int(board.get(x, y-1, 0))
    sum += 4 * int(board.get(x, y+1, 0))
    sum += 4 * int(board.get(x-1, y, 0))
    sum += 4 * int(board.get(x+1, y, 0))
    sum += int(board.get(x-1, y-1, 0))
    sum += int(board.get(x+1, y-1, 0))
    sum += int(board.get(x-1, y+1, 0))
    sum += int(board.get(x+1, y+1, 0))

    return str(int(float(sum) / 20.0))


def iterate_board(board):
    newBoard = board.new()
    for y in range(board.h):
        for x in range(board.w):
            newBoard.set(x, y, rugScore(board, x, y))
    return newBoard


a = automata(iterate=iterate_board, default_state="0")

for i in range(0, 256):
    density = 0
    if i == POP_LEVEL:
        density = POP_DENSITY
    a.new_state(str(i), i, i, ' ', density)

a.run()
