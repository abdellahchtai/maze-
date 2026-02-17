import random
from typing import Union


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


class MazeGenerator:

    """
    Class that make the maze Generate the maze with corridors
    """

    def __init__(self, width: int, height: int, entry_coord: tuple, exit_coord: tuple) -> None:

        """
        Constrocture that initialize and creat a grid from multiple Cells
        """

        self.width = width
        self.height = height
        self.entry = entry_coord
        self.exit = exit_coord
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

        while counter < (self.width + self.height):

            x = random.randint(0, self.width - 2)
            y = random.randint(0, self.height - 2)

            if self.rm_wall((x, y), (x, y + 1), 'south', 'north'):

                counter += 1
            elif self.rm_wall((x, y), (x + 1, y), 'east', 'west'):

                counter += 1

    def generate_maze(self, algo: str):

        """
        Methode that generate the maze depends on the algo that we want to use
        """
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


class MazeGenerator:

    """
    Class that make the maze Generate the maze with corridors
    """

    def __init__(self, width: int, height: int, entry_coord: tuple, exit_coord: tuple) -> None:

        """
        Constrocture that initialize and creat a grid from multiple Cells
        """

        self.width = width
        self.height = height
        self.entry = entry_coord
        self.exit = exit_coord
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

        while counter < (self.width + self.height):

            x = random.randint(0, self.width - 2)
            y = random.randint(0, self.height - 2)

            if self.rm_wall((x, y), (x, y + 1), 'south', 'north'):

                counter += 1
            elif self.rm_wall((x, y), (x + 1, y), 'east', 'west'):

                counter += 1

    def generate_maze(self, algo: str):

        """
        Methode that generate the maze depends on the algo that we want to use
        """

        try:
            self.path_42()
        except Path42Error as e:
            print(e)


        if algo == 'b':

            self.corridors_back()
        elif algo == 'p':

            self.corridors_prime()
        elif algo == 'n':

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

        self.path_42()

        if algo == 'b':

            self.corridors_back()
        elif algo == 'p':

            self.corridors_prime()
        elif algo == 'n':

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
