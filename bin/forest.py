#!/usr/bin/python3

import random
from automata import automata

# A Mathematical Approach to Forest Growth Dynamics
# http://web.math.unifi.it/users/primicer/2016%20forest%20growth

# ############# CONFIG ###################

OD = 0.2    #Old density
ND = 0.05   #New density
SD = .01    #Seed density

SF = 1     #Seed diffusivity
SP = 1     #Seed production
SG = .1     #Seed growth (0,1]
AR = .55    #Aging rate
MR = .0005   #Mortality rate
OR = .020     #Overcrowding rate


OLD_CHAR = ' '
OLD_FG = 22
OLD_BG = 22

NEW_CHAR = ' '
NEW_FG = 82
NEW_BG = 82

SEED_CHAR = '*'
SEED_FG = 222
SEED_BG = 0

EMPTY_CHAR = ' '
EMPTY_FG = 0
EMPTY_BG = 0

# ############# CONFIG #################


def new_growth(board, x, y):
    n = 0.0
    
    minx = max(0, x-1)
    maxx = min(board.w-1, x+1)
    miny = max(0, y-1)
    maxy = min(board.h-1, y+1)

    for y2 in range(miny, maxy+1):
        for x2 in range(minx, maxx+1):
            if board.get(x2,y2) == "empty":
                n += SG
    return n


def iterateBoard(board):
    global OD, ND, SD
    NOT = (SP * SG * (1-OR)) - (OR * ND) - (AR * ND)
    OOT = (AR * ND) - (MR * OD)
    SOT = (SF * SD) - (SP * SD) + (SP * OD)

    newBoard = board.copy()
    for y in range(board.h):
        for x in range(board.w):
            
            if board.get(x,y) == "old":         #OLD
                if MR > random.random():
                    newBoard.set(x,y,"empty")

            elif board.get(x,y) == "new":       #NEW
                oc = board.neighbors(x,y).count("old") * OR
                if oc > random.random():
                    newBoard.set(x,y,"empty")
                elif OOT > random.random():
                    newBoard.set(x,y,"old")

            elif board.get(x,y) == "empty":     #EMPTY
                if SOT > random.random():
                    newBoard.set(x,y,"seed")

            elif board.get(x,y) == "seed":      #SEED
                ng = board.neighbors(x,y).count("empty") * NOT
                if ng > random.random():
                    newBoard.set(x,y,"new")
                else:
                    newBoard.set(x,y,"empty")
    ND = NOT
    OD = OOT
    SD = SOT
    return newBoard






board = automata(iterate=iterateBoard, default_state="empty")
board.newState("old", OLD_FG, OLD_BG, OLD_CHAR, OD)
board.newState("new", NEW_FG, NEW_BG, NEW_CHAR, ND)
board.newState("seed", SEED_FG, SEED_BG, SEED_CHAR, 0)
board.newState("empty", EMPTY_FG, EMPTY_BG, EMPTY_CHAR, 0)
board.run()
