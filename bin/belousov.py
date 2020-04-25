#!/usr/bin/python3

from automata import automata

# Belousov-Zhabotinsky Reaction
# https://softologyblog.wordpress.com/2017/02/04/the-belousov-zhabotinsky-reaction-and-the-hodgepodge-machine/
# http://www.fractaldesign.net/AutomataAlgorithm.aspx

# ################ CONFIG #################

INFECTED_POP_LEVEL = 1
INFECTED_POP_DENSITY = 0.001

# Due to limitation of colors don't put this higher than 255
ILL_LEVEL = 255

K1 = 1  # potency of infected neighbors
K2 = 1  # potency of ill neighbors
G = 30  # progression of illness naturally

WRAP_BOARD = True

# ################ CONFIG #################


def illScore(board, x, y):

    minx = x-1
    maxx = x+1
    miny = y-1
    maxy = y+1

    a = 0.0
    b = 0.0
    s = 0.0

    state = int(board.get(x, y))
    if state >= ILL_LEVEL:
        return "0"

    for y2 in range(miny, maxy+1):
        for x2 in range(minx, maxx+1):
            if (x != x2 or y != y2):
                lvl = int(board.get(x2, y2, wrap=WRAP_BOARD, default=0))
                s += lvl
                if lvl > 0 and lvl < ILL_LEVEL:
                    a += 1.0
                elif lvl == ILL_LEVEL:
                    b += 1.0

    if state <= 0.0:
        state = int(a/K1) + int(b/K2)
    else:
        state = int(s/(a + b + 1)) + G

    if state > ILL_LEVEL:
        state = ILL_LEVEL
    return str(int(state))


def iterateBoard(board):
    newBoard = board.new()

    for y in range(board.h):
        for x in range(board.w):
            newBoard.set(x, y, illScore(board, x, y))
    return newBoard


a = automata(iterate=iterateBoard, default_state="0")

for i in range(0, ILL_LEVEL+1):
    density = 0
    if i == INFECTED_POP_LEVEL:
        density = INFECTED_POP_DENSITY
    a.newState(str(i), i, i, ' ', density)

a.run()
