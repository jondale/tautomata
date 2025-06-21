#!/usr/bin/env python3

import random
from automata import automata

# A Mathematical Approach to Forest Growth Dynamics
# http://web.math.unifi.it/users/primicer/2016%20forest%20growth

# ############# CONFIG ###################

OD = 0.9    #Old density
ND = 0.05   #New density
SD = .01    #Seed density

SF = 1     #Seed diffusivity
SP = 1     #Seed production
SG = .1     #Seed growth (0,1]
AR = .25    #Aging rate
MR = .0005   #Mortality rate
OR = .010     #Overcrowding rate

FP = .000001  #Fire probabiltiy
BP = .2      #Burnt probability
IP = .45     #Ignite probability



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

FIRE_CHAR = '^'
FIRE_FG = 52
FIRE_BG = 9

BURNT_CHAR = 'x'
BURNT_FG = 0
BURNT_BG = 52

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


def iterate_board(board):
    global OD, ND, SD
    NOT = (SP * SG * (1-OR)) - (OR * ND) - (AR * ND)
    OOT = (AR * ND) - (MR * OD)
    SOT = (SF * SD) - (SP * SD) + (SP * OD)

    newBoard = board.copy()
    for y in range(board.h):
        for x in range(board.w):
            rx=random.randrange(0,board.w)
            ry=random.randrange(0,board.h)
            if random.random() < FP:
                newBoard.set(rx,ry, "fire")

            
            if board.get(x,y) == "old":         #OLD
                fs = board.neighbors(x,y).count("fire") * IP
                if fs > random.random():
                    newBoard.set(x,y,"fire")
                elif MR > random.random():
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
            
            elif board.get(x, y) == "fire":     #FIRE
                if BP > random.random():
                    newBoard.set(x, y, "burnt")

            elif board.get(x,y) == "burnt":     #BURNT
                if SOT > random.random():
                    newBoard.set(x,y, "seed")



    ND = NOT
    OD = OOT
    SD = SOT
    return newBoard






board = automata(iterate=iterate_board, default_state="empty")
board.new_state("old", OLD_FG, OLD_BG, OLD_CHAR, OD)
board.new_state("new", NEW_FG, NEW_BG, NEW_CHAR, ND)
board.new_state("seed", SEED_FG, SEED_BG, SEED_CHAR, 0)
board.new_state("empty", EMPTY_FG, EMPTY_BG, EMPTY_CHAR, 0)
board.new_state("fire", FIRE_FG, FIRE_BG, FIRE_CHAR, 0)
board.new_state("burnt", BURNT_FG, BURNT_BG, BURNT_CHAR, 0)

board.run()
