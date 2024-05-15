#!/usr/bin/python3

import random
import time
import curses
import _curses
import traceback


class automata_board(object):
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

    def set_board(self, board):
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

    def neighbors(self, x, y, neighborhood=1):
        minx = x-neighborhood
        maxx = x+neighborhood+1
        miny = y-neighborhood
        maxy = y+neighborhood+1

        n = []
        for y2 in range(miny, maxy):
            for x2 in range(minx, maxx):
                if x2 != x or y2 != y:
                    n.append(self.get(x2, y2))

        return n

    def copy(self):
        tmp = self.board.copy()
        newBoard = automata_board(self.w, self.h, self.default, self.wrap)
        newBoard.board = tmp.copy()
        self.board = tmp.copy()
        return newBoard

    def new(self):
        tmp = self.board.copy()
        newBoard = automata_board(self.w, self.h, self.default, self.wrap)
        self.board = tmp.copy()
        return newBoard

    def print(self):
        for y in range(self.h):
            for x in range(self.w):
                print(str(self.get(x, y))+" ", end='')
            print("")


class automata:
    message_timeout = 2
    delay = 0.15
    delay_max = 1
    delay_min = 0.01
    delay_delta = 0.05
    states = {}
    default_state = None
    board = None
    scr = None
    h = 0
    w = 0
    msg = None
    msg_time = 0
    iterate_function = None
    init_function = None
    post_init_function = None

    def __init__(self, iterate, default_state, init=None, post_init=None):
        self.iterate_function = iterate
        self.default_state = default_state
        self.init_function = init
        self.post_init_function = post_init

    def __del__(self):
        if self.scr:
            self.scr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def init_screen(self):
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

    def new_state(self, state, fg, bg, char, percent):
        if not isinstance(char, int):
            char = ord(char)
        self.states[state] = {
            'fg': fg,
            'bg': bg,
            'char': char,
            'percent': percent
        }

    def notify(self, m):
        self.msg = m
        self.msg_time = time.time()

    def init_board(self):
        self.board = automata_board(self.w, self.h, self.default_state)
        if self.init_function:
            self.board.set_board(self.init_function(self.board))
        else:
            for y in range(self.h):
                for x in range(self.w):
                    for i in self.states:
                        s = self.states[i]
                        if random.random() < s["percent"]:
                            self.board.set(x, y, i)
                            break

        if self.post_init_function:
            self.board.set_board(self.post_init_function(self.board))

    def draw_state(self, x, y, state):
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
                self.draw_state(x, y, state)

        if self.msg:
            t = time.time()
            if (t - self.msg_time) > self.message_timeout:
                self.msg = None
                self.msg_time = 0
            else:
                try:
                    self.scr.addstr(self.h-1, 0, self.msg)
                except Exception:
                    pass
        self.scr.refresh()

    def iterate(self):
        if self.iterate_function:
            self.board = self.iterate_function(self.board)

    def run(self):
        try:

            self.init_screen()
            self.init_board()
            last_update = 0
            while True:
                char = self.scr.getch()
                if char == ord('q'):
                    break
                elif char == curses.KEY_UP:
                    self.delay += self.delay_delta
                    if self.delay > self.delay_max:
                        self.delay = self.delay_max
                    self.notify("delay: {:.2f}".format(self.delay))
                elif char == curses.KEY_DOWN:
                    self.delay -= self.delay_delta
                    if self.delay <= self.delay_min:
                        self.delay = self.delay_min
                    self.notify("delay: {:.2f}".format(self.delay))
                elif char > 0:
                    self.init_screen()
                    self.init_board()

                t = time.time()
                if (t - last_update) >= self.delay:
                    self.draw()
                    self.iterate()
                    last_update = t
                time.sleep(self.delay_min)

        except Exception as e:
            self.__del__()
            traceback.print_exc()
            print(e)
            quit()
