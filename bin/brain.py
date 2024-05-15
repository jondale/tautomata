#!/usr/bin/python3

from automata import automata

# https://en.wikipedia.org/wiki/Brian's_Brain

# ################ CONFIG #################

# How dense to orinally populate the board.
# .25 seems to give best results
CHANCE_OF_LIFE = .25

WRAP_BOARD = True

LIVE_CHAR = ' '
LIVE_FG = 254
LIVE_BG = 45
DYING_CHAR = ' '
DYING_FG = 0
DYING_BG = 20
DEAD_CHAR = ' '
DEAD_FG = 233
DEAD_BG = 16

# ################ CONFIG #################


def iterateLife(board):
    board.wrap = WRAP_BOARD
    newBoard = board.new()
    for y in range(board.h):
        for x in range(board.w):
            n = board.neighbors(x, y).count("live")
            state = board.get(x, y)
            if state == "live":
                newBoard.set(x, y, "dying")
            elif state == "dying":
                newBoard.set(x, y, "dead")
            elif state == "dead" and n == 2:
                newBoard.set(x, y, "live")
    return newBoard.copy()


a = automata(iterate=iterateLife, default_state="dead")
a.new_state("live", LIVE_FG, LIVE_BG, LIVE_CHAR, CHANCE_OF_LIFE)
a.new_state("dying", DYING_FG, DYING_BG, DYING_CHAR, 0)
a.new_state("dead", DEAD_FG, DEAD_BG, DEAD_CHAR, 0)
a.run()
