import curses
import time
from maze_generator import MazeGenerator
import sys


def ft_render(config: dict) -> MazeGenerator:
    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry_coord = config["ENTRY"]
    exit_coord = config["EXIT"]
    perfect = config["PERFECT"]

    path = None
    maze = MazeGenerator(width, height, entry_coord, exit_coord, perfect)
    maze.generate_maze(True)
    animated = True
    while True:
        try:
            action = curses.wrapper(draw_maze, maze, path, animated)
            if action == "QUIT":
                break
            if action == "REGENERATE":
                maze = MazeGenerator(width, height,
                                     entry_coord, exit_coord, perfect)
                maze.generate_maze(False)
                path = None
                animated = True
            if action == "PATH":
                # if path is None:2
                if path is not None:
                    path = None
                else:
                    path = maze.path_finder()
                animated = False
                # else:
                #     path = None
        except (RecursionError, KeyboardInterrupt):
            print("The width or the height are too big try with smaller values")
            sys.exit(1)

    return maze


def safe_addch(stdscr, y, x, ch, attr=0):
    h, w = stdscr.getmaxyx()
    if 0 <= y < h and 0 <= x < w:
        try:
            stdscr.addch(y, x, ch, attr)
        except curses.error:
            pass


def safe_addstr(stdscr, y, x, text, attr=0):
    h, w = stdscr.getmaxyx()
    if 0 <= y < h and 0 <= x < w:
        try:
            stdscr.addstr(y, x, text[: w - x], attr)
        except curses.error:
            pass


def draw_maze(stdscr, maze, path, animated: bool) -> str | None:
    curses.curs_set(0)            # hide the blinking cursor
    stdscr.nodelay(True)          # don't block on getch()
    stdscr.timeout(100)           # wait 100ms between refreshes
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(0, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(42, curses.COLOR_BLACK, curses.COLOR_WHITE)
    CELL_HEIGHT = 2
    CELL_WIDTH = 2
    grid = maze.grid
    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit
    animate = animated
    rows = maze.width
    cols = maze.height
    total_cells = rows * cols 

    TARGET_DURATION = 1.2
    delay = TARGET_DURATION / total_cells
    delay = max(0.002, min(delay, 0.05))
    current_color = 0
    current_color_index = 0
    COLOR_PAIRS = [3, 4, 5, 6]

    try:
        while True:
            
            maze_width = cols * CELL_WIDTH + 1
            maze_height = rows * CELL_HEIGHT + 1
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            start_x = (width - maze_width) // 2
            start_y = (height - maze_height) // 2
            if height >= maze_height + start_y + 7 and width >= maze_width:
                for row_index, row in enumerate(grid):
                    if animate:
                        time.sleep(delay)
                    for col_index, cell in enumerate(row):
                        if animate:
                            time.sleep(delay)
                            stdscr.refresh()
                        screen_y = row_index * CELL_HEIGHT + 1 + start_y
                        screen_x = col_index * CELL_WIDTH + 1 + start_x
                        safe_addch(stdscr, screen_y - 1, 0 + start_x, "░",
                                   curses.color_pair(current_color))
                        safe_addch(stdscr, screen_y, 0 + start_x, "░", curses.color_pair(current_color))
                        safe_addch(stdscr, screen_y + 1, 0 + start_x, "░", curses.color_pair(current_color))
                        safe_addch(stdscr, 0 + start_y, screen_x, "░", curses.color_pair(current_color))
                        safe_addch(stdscr, 0 + start_y, screen_x + 1, "░", curses.color_pair(current_color))
                        safe_addch(stdscr, screen_y + 1, screen_x + 1, "░", curses.color_pair(current_color))

                        if cell.path_42:
                            safe_addch(stdscr, screen_y, screen_x, ' ',curses.color_pair(42))
                        if cell.north:
                            safe_addch(stdscr, screen_y - 1, screen_x, "░", curses.color_pair(current_color))
                        if cell.south is True:
                            safe_addch(stdscr, screen_y + 1, screen_x, "░", curses.color_pair(current_color))
                        if cell.west is True:
                            safe_addch(stdscr, screen_y, screen_x - 1, "░", curses.color_pair(current_color))
                        if cell.east is True:
                            safe_addch(stdscr, screen_y, screen_x + 1, "░", curses.color_pair(current_color))

                safe_addstr(stdscr, height -7, 0, "==== A-Maze-ing ====")
                safe_addstr(stdscr, height -6, 0, "0. Animate")
                safe_addstr(stdscr, height -5, 0, "1. Re-generate a new maze.")
                safe_addstr(stdscr, height -4, 0, "2. Show/Hide path from entry to exit.")
                safe_addstr(stdscr, height -3, 0, "3. Rotate maze colors")
                safe_addstr(stdscr, height -2, 0, "4. Quit.")
                safe_addstr(stdscr, height -1, 0, "Choise? (0-4)")
            else:  
                safe_addstr(stdscr, 0, 0, "Terminal is too small")
            if height >= maze_height + start_y + 7 and width >= maze_width:
                safe_addch(stdscr, entry_y * CELL_WIDTH + start_y + 1, entry_x * CELL_WIDTH + start_x + 1, ' ',curses.color_pair(1))
                if animate:
                    stdscr.refresh()
                    time.sleep(0.5)
                safe_addch(stdscr, exit_y * CELL_WIDTH + start_y + 1, exit_x * CELL_WIDTH + start_x + 1, ' ',curses.color_pair(2))
                if path is not None:
                    if animate:
                        stdscr.refresh()
                        time.sleep(0.5)

                    i = 0
                    while i < len(path) - 1:
                        if animate:
                            stdscr.refresh()
                            time.sleep(0.1)
                        x0, y0 = path[i]
                        x1, y1 = path[i + 1]

                        screen_y = y0 * CELL_HEIGHT + 1 + start_y
                        screen_x = x0 * CELL_HEIGHT + 1 + start_x

                        if y1 == y0 and x1 < x0:
                            safe_addch(stdscr, screen_y, screen_x - 1,
                                       "░", curses.color_pair(7))
                        if y1 == y0 and x1 > x0:
                            safe_addch(stdscr, screen_y, screen_x + 1, "░", curses.color_pair(7))
                        if y1 < y0 and x1 == x0:
                            safe_addch(stdscr, screen_y - 1 , screen_x, "░", curses.color_pair(7))
                        if y1 > y0 and x1 == x0:
                            safe_addch(stdscr, screen_y + 1, screen_x, "░", curses.color_pair(7))
                        safe_addch(stdscr, screen_y, screen_x, "░", curses.color_pair(7))
                        safe_addch(stdscr, entry_y * CELL_WIDTH + start_y + 1, entry_x * CELL_WIDTH + start_x + 1, ' ',curses.color_pair(1))
                        safe_addch(stdscr, exit_y * CELL_WIDTH + start_y + 1, exit_x * CELL_WIDTH + start_x + 1, ' ',curses.color_pair(2))
                        i += 1
        
            stdscr.refresh()
            animate = False

            # Get user input
            key = stdscr.getch()
            if key == ord('0'):
                animate = True
            if key == ord('4'):
                return "QUIT"
            if key == ord('3'):
                current_color_index = (current_color_index + 1) % len(COLOR_PAIRS)
                current_color = COLOR_PAIRS[current_color_index]
            if key == ord('2'):
                return "PATH"
            if key == ord('1'):
                return "REGENERATE"
            if key == curses.KEY_RESIZE:
                stdscr.clear()
                continue

    except (KeyboardInterrupt):
        return "QUIT"
