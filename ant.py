#!/usr/bin/python3

from automata import automata

# https://en.wikipedia.org/wiki/Langton's_ant

# ################ CONFIG #################

S1_CHAR = ' '
S1_FG = 16
S1_BG = 45

S2_CHAR = ' '
S2_FG = 45
S2_BG = 16

ANT_CHAR = '*'

# ################ CONFIG #################


def iterateLife(board):
    newBoard = board.copy()
    for y in range(board.h):
        for x in range(board.w):
            state = board.get(x, y)
            if state not in ("s1", "s2"):
                a, d, s = state.split(".")
                if s == "s1":
                    if d == "west":
                        newdir = "north"
                        y2 = y + 1
                        x2 = x
                    elif d == "north":
                        newdir = "east"
                        x2 = x + 1
                        y2 = y
                    elif d == "east":
                        newdir = "south"
                        y2 = y - 1
                        x2 = x
                    else:
                        newdir = "west"
                        y2 = y
                        x2 = x - 1
                    newBoard.set(x, y, "s2", wrap=True)
                else:
                    if d == "west":
                        newdir = "south"
                        y2 = y - 1
                        x2 = x
                    elif d == "north":
                        newdir = "west"
                        x2 = x - 1
                        y2 = y
                    elif d == "east":
                        newdir = "north"
                        y2 = y + 1
                        x2 = x
                    else:
                        newdir = "east"
                        y2 = y
                        x2 = x + 1
                    newBoard.set(x, y, "s1")
                oldstate = board.get(x2, y2, wrap=True)
                newstate = "ant.{}.{}".format(newdir, oldstate)
                newBoard.set(x2, y2, newstate, wrap=True)
    return newBoard.copy()


def postInit(board):
    x = int(board.w / 2)
    y = int(board.h / 2)
    board.set(x, y, "ant.east.s1")
    return board


a = automata(postInit=postInit, iterate=iterateLife, default_state="s2")
a.newState("s1", S1_FG, S1_BG, S1_CHAR, 0)
a.newState("s2", S2_FG, S2_BG, S2_CHAR, 0)
a.newState("ant.west.s1", S1_FG, S1_BG, ANT_CHAR, 0)
a.newState("ant.south.s1", S1_FG, S1_BG, ANT_CHAR, 0)
a.newState("ant.east.s1", S1_FG, S1_BG, ANT_CHAR, 0)
a.newState("ant.north.s1", S1_FG, S1_BG, ANT_CHAR, 0)
a.newState("ant.west.s2", S2_FG, S2_BG, ANT_CHAR, 0)
a.newState("ant.south.s2", S2_FG, S2_BG, ANT_CHAR, 0)
a.newState("ant.east.s2", S2_FG, S2_BG, ANT_CHAR, 0)
a.newState("ant.north.s2", S2_FG, S2_BG, ANT_CHAR, 0)
a.run()
