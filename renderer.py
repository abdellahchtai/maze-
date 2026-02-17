import curses
import time


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


def draw_maze(stdscr, maze) -> None:
    curses.curs_set(0)            # hide the blinking cursor
    stdscr.nodelay(True)          # don't block on getch()
    stdscr.timeout(100)           # wait 100ms between refreshes
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(42, curses.COLOR_BLACK, curses.COLOR_GREEN)
    CELL_HEIGHT = 2
    CELL_WIDTH = 2
    grid = maze.grid
    entry_x, entry_y = maze.entry
    exit_x, exit_y = maze.exit
    animate = True
    rows = maze.width
    cols = maze.height
    total_cells = rows * cols

    TARGET_DURATION = 1.2
    delay = TARGET_DURATION / total_cells
    delay = max(0.002, min(delay, 0.05))
    try:
        while True:
            
            maze_width = cols* CELL_WIDTH + 1
            maze_height = rows * CELL_HEIGHT + 1
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            start_x = (width - maze_width) // 2
            start_y = (height - maze_height) // 2
            if height >= maze_height + start_y + 6 and width >= maze_width:
                for row_index, row in enumerate(grid):
                    if animate:
                        time.sleep(delay)
                    for col_index, cell in enumerate(row):
                        if animate:
                            time.sleep(delay)
                            stdscr.refresh()
                        screen_y = row_index * CELL_HEIGHT + 1 + start_y
                        screen_x = col_index * CELL_WIDTH + 1 + start_x
                        safe_addch(stdscr, screen_y - 1, 0 + start_x, "░", )
                        safe_addch(stdscr, screen_y, 0 + start_x, "░")
                        safe_addch(stdscr, screen_y + 1, 0 + start_x, "░")
                        safe_addch(stdscr, 0 + start_y, screen_x, "░")
                        safe_addch(stdscr, 0 + start_y, screen_x + 1, "░")
                        safe_addch(stdscr, screen_y + 1, screen_x + 1, "░") 

                        if cell.path_42:
                            safe_addch(stdscr, screen_y, screen_x, ' ',curses.color_pair(42))
                        if cell.north:
                            safe_addch(stdscr, screen_y - 1, screen_x, "░")
                        if cell.south is True:
                            safe_addch(stdscr, screen_y + 1, screen_x, "░")
                        if cell.west is True:
                            safe_addch(stdscr, screen_y, screen_x - 1, "░")
                        if cell.east is True:
                            safe_addch(stdscr, screen_y, screen_x + 1, "░")

                safe_addstr(stdscr, height -6, 0, f"==== A-Maze-ing === ENTRY({entry_x}, {entry_y})")
                safe_addstr(stdscr, height -5, 0, "1. Re-generate a new maze.")
                safe_addstr(stdscr, height -4, 0, "2. Show/Hide path from entry to exit.")
                safe_addstr(stdscr, height -3, 0, "3. Rotate maze colors")
                safe_addstr(stdscr, height -2, 0, "4. Quit.")
                safe_addstr(stdscr, height -1, 0, "Choise? (1-4)")
            else:  
                safe_addstr(stdscr, 0, 0, "Terminal is too small")
            if height >= maze_height + start_y + 6 and width >= maze_width:
                safe_addch(stdscr, entry_y * CELL_WIDTH + start_y + 1, entry_x * CELL_WIDTH + start_x + 1, ' ',curses.color_pair(1))
                safe_addch(stdscr, exit_y * CELL_WIDTH + start_y + 1, exit_x * CELL_WIDTH + start_x + 1, ' ',curses.color_pair(2))
            stdscr.refresh()
            animate = False

            # Get user input
            key = stdscr.getch()
            if key == ord('a'):
                animate = True
            if key == ord('4'):
                break               
            if key == ord('3'):
                continue
            if key == ord('2'):
                continue
            if key == ord('1'):
                from a_maze_ing import MazeGenerator
                maze0 = MazeGenerator(maze.width, maze.height, maze.entry, maze.exit)
                maze0 = maze.generate_maze("b")
                stdscr.clear()
                curses.wrapper(draw_maze, maze0)
            if key == curses.KEY_RESIZE:
                stdscr.clear()
                continue

    except (KeyboardInterrupt):
        pass


