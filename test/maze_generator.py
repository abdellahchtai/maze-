import random
from typing import Union
from collections import deque


class Path42Error(Exception):

    """
    Class Path42Error to custom the error
    for space ths is not enough to hold 42 pattern
    """
    pass


class Cell:

    """
    Class for creating independant Cell
    """

    def __init__(self) -> None:

        """
        Constroctur to initiliaze the walls of the Cell as close (True) and
        not visited (False)
        """

        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False
        self.path_42 = False
        self.BFSvisited = False
        self.parent = None


class MazeGenerator:

    """
    Class that make the maze Generate the maze with corridors
    """

    def __init__(self, width: int, height: int,
                 entry: tuple, exit: tuple, perfect: bool) -> None:

        """
        Constrocture that initialize and creat a grid from multiple Cells
        """

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]

    def rm_wall(self, pos1: tuple, pos_2: tuple, d1: str, d_2: str) -> bool:

        """
        Method that remove the wall of the Cell in a specifique direction
        and remove also the wall of the other Cell that face the main Cell
        """
        if (
            not self.grid[pos1[1]][pos1[0]].path_42 and
            not self.grid[pos_2[1]][pos_2[0]].path_42
        ):
            self.grid[pos1[1]][pos1[0]].__dict__[d1] = False
            self.grid[pos_2[1]][pos_2[0]].__dict__[d_2] = False
            return True

        return False

    def neighbor_back(self, cord: tuple = (0, 0)) -> Union[list, None]:

        """
        Methode that return all valid neighbor of the cord and return
        random one
        """

        valid = list()

        if (
            cord[1] > 0 and not
            (self.grid[cord[1] - 1][cord[0]].visited)
            and not (self.grid[cord[1] - 1][cord[0]].path_42)
        ):

            valid.append([cord[0], cord[1] - 1, 'n'])

        if (
            cord[1] + 1 < self.height and not
            (self.grid[cord[1] + 1][cord[0]].visited)
            and not (self.grid[cord[1] + 1][cord[0]].path_42)
        ):

            valid.append([cord[0], cord[1] + 1, 's'])

        if (
            cord[0] > 0 and not
            (self.grid[cord[1]][cord[0] - 1].visited)
            and not (self.grid[cord[1]][cord[0] - 1].path_42)
        ):

            valid.append([cord[0] - 1, cord[1], 'w'])

        if (
            cord[0] + 1 < self.width and not
            (self.grid[cord[1]][cord[0] + 1].visited)
            and not (self.grid[cord[1]][cord[0] + 1].path_42)
        ):

            valid.append([cord[0] + 1, cord[1], 'e'])

        if not len(valid):
            return None

        return random.choice(valid)

    def corridors_back(self, pos: tuple = (0, 0)) -> None:

        """
        Methode that creat corridors using backtracker algo
        """

        self.grid[pos[1]][pos[0]].visited = True
        valid = self.neighbor_back(pos)

        while valid:
            if valid[2] == 'n':

                self.rm_wall(pos, (valid[0], valid[1]), 'north', 'south')
            elif valid[2] == 's':

                self.rm_wall(pos, (valid[0], valid[1]), 'south', 'north')
            elif valid[2] == 'e':

                self.rm_wall(pos, (valid[0], valid[1]), 'east', 'west')
            elif valid[2] == 'w':

                self.rm_wall(pos, (valid[0], valid[1]), 'west', 'east')

            self.corridors_back((valid[0], valid[1]))
            valid = self.neighbor_back(pos)

    def neighbor_prime(self, valid: list,
                       cord: tuple = (0, 0)) -> Union[list, None]:
        """
        Methode that return all valid neighbor of the cord and return
        random one
        """

        if (
            cord[1] > 0 and not
            (self.grid[cord[1] - 1][cord[0]].visited)
            and not (self.grid[cord[1] - 1][cord[0]].path_42)
        ):

            valid.append((cord[0], cord[1] - 1))

        if (
            cord[1] + 1 < self.height and not
            (self.grid[cord[1] + 1][cord[0]].visited)
            and not (self.grid[cord[1] + 1][cord[0]].path_42)
        ):

            valid.append((cord[0], cord[1] + 1))

        if (
            cord[0] > 0 and not
            (self.grid[cord[1]][cord[0] - 1].visited)
            and not (self.grid[cord[1]][cord[0] - 1].path_42)
        ):

            valid.append((cord[0] - 1, cord[1]))

        if (
            cord[0] + 1 < self.width and not
            (self.grid[cord[1]][cord[0] + 1].visited)
            and not (self.grid[cord[1]][cord[0] + 1].path_42)
        ):

            valid.append((cord[0] + 1, cord[1]))

        return valid

    def closest_neib(self, cord: tuple) -> Union[str, None]:

        """
        Method that return the closest neighbor for the Cell
        with cordinates (cord)
        """

        direct = list()

        if (
            cord[1] - 1 >= 0 and self.grid[cord[1] - 1][cord[0]].visited
            and not (self.grid[cord[1] - 1][cord[0]].path_42)
        ):

            direct.append('n')
        if (
            cord[1] + 1 < self.height
            and self.grid[cord[1] + 1][cord[0]].visited
            and not (self.grid[cord[1] + 1][cord[0]].path_42)
        ):

            direct.append('s')
        if (
            cord[0] - 1 >= 0 and self.grid[cord[1]][cord[0] - 1].visited
            and not (self.grid[cord[1]][cord[0] - 1].path_42)
        ):

            direct.append('w')
        if (
            cord[0] + 1 < self.width
            and self.grid[cord[1]][cord[0] + 1].visited
            and not (self.grid[cord[1]][cord[0] + 1].path_42)
        ):

            direct.append('e')

        if len(direct):
            return random.choice(direct)

        return None

    def rm_wall_prime(self, dir: str, pos1: tuple) -> bool:

        """
        Method that remove wall in specifique direction (dir),
        in case of seccusse it return true
        """

        if dir == 'n':

            return self.rm_wall(pos1, (pos1[0], pos1[1] - 1), 'north', 'south')
        elif dir == 's':

            return self.rm_wall(pos1, (pos1[0], pos1[1] + 1), 'south', 'north')
        elif dir == 'e':

            return self.rm_wall(pos1, (pos1[0] + 1, pos1[1]), 'east', 'west')
        elif dir == 'w':

            return self.rm_wall(pos1, (pos1[0] - 1, pos1[1]), 'west', 'east')

    def corridors_prime(self, pos1: tuple = (0, 0)):

        """
        Methode that return all valid neighbor of the Cell and add it to the
        old ones and return everything
        """

        valid2 = list()

        self.grid[pos1[1]][pos1[0]].visited = True

        valid2 = self.neighbor_prime(valid2, pos1)

        while valid2:

            pos2 = random.choice(valid2)
            dir = self.closest_neib(pos2)

            if dir:

                if self.rm_wall_prime(dir, pos2):

                    self.grid[pos2[1]][pos2[0]].visited = True
                    valid2 = self.neighbor_prime(valid2, pos2)

                valid2.remove(pos2)

            else:

                valid2.remove(pos2)

            valid2 = list(set(valid2))

    def corridors_unperfect(self, corr: tuple = (0, 0)) -> None:

        """
        Methode that create the maze with multiple way (none perfect maze)
        """

        self.corridors_prime(corr)

        counter = 0

        while counter < self.width * self.height * 0.10:

            x = random.randint(0, self.width - 2)
            y = random.randint(0, self.height - 2)

            if self.rm_wall((x, y), (x, y + 1), 'south', 'north'):

                counter += 1
            elif self.rm_wall((x, y), (x + 1, y), 'east', 'west'):

                counter += 1

    def generate_maze(self, flag) -> None:

        """
        Methode that generate the maze depends on the algo that we want to use
        """

        try:
            self.path_42()
        except Path42Error as e:
            if flag:
                print(e)

        if self.perfect:

            self.corridors_back()

        else:

            self.corridors_unperfect()

    def path_42(self):

        """
        Methode that make the 42 pattern
        """

        if self.width < 9 or self.height < 9:
            raise Path42Error('Invalid space for creating 42 pattern')

        st1 = self.width // 2 - 3
        st2 = self.height // 2 - 2

        for i in range(2):
            self.grid[st2 + i][st1].path_42 = True

        for i in range(3):
            self.grid[st2 + 2][st1 + i].path_42 = True

        for i in range(2):
            self.grid[st2 + 3 + i][st1 + 2].path_42 = True

        st1 += 4

        for i in range(2):
            self.grid[st2][st1 + i].path_42 = True

        for i in range(2):
            self.grid[st2 + i][st1 + 2].path_42 = True

        for i in range(2):
            self.grid[st2 + 2][st1 + 2 - i].path_42 = True

        for i in range(2):
            self.grid[st2 + 2 + i][st1].path_42 = True

        for i in range(3):
            self.grid[st2 + 4][st1 + i].path_42 = True

    def init_new(self) -> None:

        """
        Helper methode that initialize and add new atrributes to the
        maze for finding the path
        """

        for row in self.grid:

            for cell in row:

                cell.seen = False
                cell.parent = None

    def path_finder(self) -> list:

        """
        Methode that find the shoretest path from the entry to the exit
        """

        self.init_new()
        cord = deque([self.entry])
        x, y = self.entry
        self.grid[y][x].seen = True

        while cord:

            x, y = cord.popleft()

            if (x, y) == self.exit:
                break

            next_move = (
                (self.grid[y][x].north, x, y - 1),
                (self.grid[y][x].east, x + 1, y),
                (self.grid[y][x].south, x, y + 1),
                (self.grid[y][x].west, x - 1, y)
            )

            for wall, new_x, new_y in next_move:
                if (0 <= new_x < self.width and 0 <= new_y < self.height
                   and not wall and not self.grid[new_y][new_x].seen):
                    self.grid[new_y][new_x].seen = True
                    cord.append((new_x, new_y))
                    self.grid[new_y][new_x].parent = (x, y)

        path = []
        path.append((x, y))
        while (x, y) != self.entry:
            x, y = self.grid[y][x].parent
            path.append((x, y))

        path.reverse()
        return path
