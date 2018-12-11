import cv2
import curses
import numpy as np
from ascii_convert import *

def drawScreen(stdscr):
    # clear screen
    term_height, term_width = stdscr.getmaxyx()
    stdscr.refresh()
    # set colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # Get rid of cursor
    curses.curs_set(0)
    stdscr.clear
    # Turn color on Current default color but I will make it changable default too
    stdscr.attron (curses.color_pair (2))
    # Add a box around screen
    stdscr.box()
    # Print to screen
    stdscr.addstr("=> Press esc to quit.")

    cap = cv2.VideoCapture(0)
    v_width, v_height = (0, 0)
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    else:
        # get cap property height and width
        v_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
        v_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float

    # Set the resolution of the window for the ascii conversion
    converter = AsciiConvert(term_width-2, term_height-2, False)
    string = str(term_width) + ' ' + str(term_height) + ' ' + str(v_width) + ' ' + str(v_height)
    string_len = len(string)
    stdscr.addstr(term_height - 1, term_width - 1 - string_len, string)

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # resize for curses
        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Convert fram
        converter.convertFrame(gray_frame)
        # Print frame
        converter.printToScreen(stdscr, 1, 1)
        # Wait for next input
        stdscr.refresh()
        stdscr.timeout(30)
        k = stdscr.getch()
        if k == 27:
            break
    # Turn off color
    stdscr.attroff (curses.color_pair (2))
    cap.release()
    # Return Cursor
    curses.curs_set(1)

def main():
    curses.wrapper(drawScreen)

if __name__ == "__main__":
    main()
