#!/usr/bin/python3
import curses


def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, 0, i)
    try:
        for i in range(1, 257):
            stdscr.addstr(' '+str(i-1)+' ', curses.color_pair(i))
    except curses.ERR:
        # End of screen reached
        pass
    stdscr.getch()


curses.wrapper(main)
