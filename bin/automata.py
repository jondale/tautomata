#!/usr/bin/python3

import random
import time
import curses
import _curses
import traceback


class automataBoard(object):
    board = []
    w = 0
    h = 0
    default = None
    wrap = False

    def __init__(self, w, h, default, wrap=False):
        self.board.clear()
        self.w = w
        self.h = h
        self.default = default
        self.wrap = wrap
        for i in range(h):
            self.board.append([])
            for j in range(w):
                self.board[i].append(default)

    def setBoard(self, board):
        self.board = board.board.copy()

    def set(self, x, y, val):
        if self.wrap:
            if x < 0:
                x += self.w
            if x >= self.w:
                x -= self.w
            if y < 0:
                y += self.h
            if y >= self.h:
                y -= self.h
        self.board[y][x] = val

    def get(self, x, y, default=None):
        if self.wrap:
            if x < 0:
                x += self.w
            if x >= self.w:
                x -= self.w
            if y < 0:
                y += self.h
            if y >= self.h:
                y -= self.h
            return self.board[y][x]
        else:
            if x < 0 or x >= self.w or y < 0 or y >= self.h:
                return default
            return self.board[y][x]

    def copy(self):
        tmp = self.board.copy()
        newBoard = automataBoard(self.w, self.h, self.default, self.wrap)
        newBoard.board = tmp.copy()
        self.board = tmp.copy()
        return newBoard

    def new(self):
        tmp = self.board.copy()
        newBoard = automataBoard(self.w, self.h, self.default, self.wrap)
        self.board = tmp.copy()
        return newBoard

    def print(self):
        for y in range(self.h):
            for x in range(self.w):
                print(str(self.get(x, y))+" ", end='')
            print("")


class automata:
    msgTimeout = 2
    delay = 0.15
    delayMax = 1
    arrowDelta = 0.05
    states = {}
    defaultState = None
    board = None
    scr = None
    h = 0
    w = 0
    msg = None
    msgTime = 0
    funcIterate = None
    funcInit = None
    funcPostInit = None

    def __init__(self, iterate, default_state, init=None, postInit=None):
        self.funcIterate = iterate
        self.defaultState = default_state
        self.funcInit = init
        self.funcPostInit = postInit

    def __del__(self):
        if self.scr:
            self.scr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def initScreen(self):
        self.scr = curses.initscr()
        self.h, self.w = self.scr.getmaxyx()
        self.scr.scrollok(False)
        self.scr.keypad(True)
        curses.curs_set(False)
        curses.noecho()
        curses.cbreak()
        self.scr.nodelay(True)
        curses.start_color()
        curses.use_default_colors()

        i = 1
        for state in self.states:
            self.states[state]["color"] = i
            fg = self.states[state]["fg"]
            bg = self.states[state]["bg"]
            curses.init_pair(i, fg, bg)
            i += 1

    def newState(self, state, fg, bg, char, percent):
        self.states[state] = {
            'fg': fg,
            'bg': bg,
            'char': ord(char),
            'percent': percent
        }

    def notify(self, m):
        self.msg = m
        self.msgTime = time.time()

    def initBoard(self):
        self.board = automataBoard(self.w, self.h, self.defaultState)
        if self.funcInit:
            self.board.setBoard(self.funcInit(self.board))
        else:
            for y in range(self.h):
                for x in range(self.w):
                    for i in self.states:
                        s = self.states[i]
                        if random.random() < s["percent"]:
                            self.board.set(x, y, i)
                            break

        if self.funcPostInit:
            self.board.setBoard(self.funcPostInit(self.board))

    def drawState(self, x, y, state):
        try:
            char = self.states[state]["char"]
            i = self.states[state]["color"]
            color = curses.color_pair(i)
            self.scr.addch(y, x, char, color)
        except _curses.error:
            pass

    def draw(self):
        for y in range(self.h):
            for x in range(self.w):
                state = self.board.get(x, y)
                self.drawState(x, y, state)

        if self.msg:
            t = time.time()
            if (t - self.msgTime) > self.msgTimeout:
                self.msg = None
                self.msgTime = 0
            else:
                try:
                    self.scr.addstr(self.h-1, 0, self.msg)
                except Exception:
                    pass
        self.scr.refresh()

    def iterate(self):
        if self.funcIterate:
            self.board = self.funcIterate(self.board)

    def run(self):
        try:

            self.initScreen()
            self.initBoard()
            last_update = 0
            while True:
                char = self.scr.getch()
                if char == ord('q'):
                    break
                elif char == curses.KEY_UP:
                    self.delay += self.arrowDelta
                    if self.delay > self.delayMax:
                        self.delay = self.delayMax
                    self.notify("delay: {:.2f}".format(self.delay))
                elif char == curses.KEY_DOWN:
                    self.delay -= self.arrowDelta
                    if self.delay <= 0:
                        self.delay = 0.01
                    self.notify("delay: {:.2f}".format(self.delay))
                elif char > 0:
                    self.initScreen()
                    self.initBoard()

                t = time.time()
                if (t - last_update) >= self.delay:
                    self.draw()
                    self.iterate()
                    last_update = t

        except Exception as e:
            self.__del__()
            traceback.print_exc()
            print(e)
            quit()
