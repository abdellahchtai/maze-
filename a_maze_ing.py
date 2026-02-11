#!/bin/env python3.10
from typing import Union
import random


class Path42Error(Exception):
    """
    Class Path42Error to custom the error of 42 pattern
    """
    pass


class cell:
    """
    Class for creating independant cell
    """
    def __init__(self) -> None:
        """
        Constroctur to initiliaze the walls of the cell as close (True) and
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
    def __init__(self, x: int, y: int) -> None:
        """
        Constrocture that initialize and creat a grid from multiple cells
        """
        self.x = x
        self.y = y
        self.maze = [[cell() for _ in range(x)] for _ in range(y)]

    def rm_wall(self, pos1: tuple, pos_2: tuple, d1: str, d_2: str) -> None:
        """
        Method that remove the wall of the cell in a specifique direction
        and remove also the wall of the other cell that face the main cell
        """
        self.maze[pos1[1]][pos1[0]].__dict__[d1] = False
        self.maze[pos_2[1]][pos_2[0]].__dict__[d_2] = False
        self.maze[pos1[1]][pos1[0]].visited = True
        self.maze[pos_2[1]][pos_2[0]].visited = True

    def neighbor(self, cord: tuple) -> Union[list, None]:
        """
        Methode that return all valid neighbor of the cord and return
        random one
        """
        valid = list()
        if (
            cord[1] > 0 and not
            (self.maze[cord[1] - 1][cord[0]].visited)
            and not (self.maze[cord[1] - 1][cord[0]].path_42)
        ):
            valid.append([cord[0], cord[1] - 1, 'n'])
        if (
            cord[1] + 1 < self.y and not
            (self.maze[cord[1] + 1][cord[0]].visited)
            and not (self.maze[cord[1] + 1][cord[0]].path_42)
        ):
            valid.append([cord[0], cord[1] + 1, 's'])
        if (
            cord[0] > 0 and not
            (self.maze[cord[1]][cord[0] - 1].visited)
            and not (self.maze[cord[1]][cord[0] - 1].path_42)
        ):
            valid.append([cord[0] - 1, cord[1], 'w'])
        if (
            cord[0] + 1 < self.x and not
            (self.maze[cord[1]][cord[0] + 1].visited)
            and not (self.maze[cord[1]][cord[0] + 1].path_42)
        ):
            valid.append([cord[0] + 1, cord[1], 'e'])

        if not len(valid):
            return None

        return random.choice(valid)

    def corridors(self, pos: tuple = (0, 0), flag=False) -> None:
        """
        Methode that creat corridors
        """
        if not flag:
            self.path_42()
            flag = True

        valid = self.neighbor(pos)

        while valid:
            if valid[2] == 'n':
                self.rm_wall(pos, (valid[0], valid[1]), 'north', 'south')
            elif valid[2] == 's':
                self.rm_wall(pos, (valid[0], valid[1]), 'south', 'north')
            elif valid[2] == 'e':
                self.rm_wall(pos, (valid[0], valid[1]), 'east', 'west')
            elif valid[2] == 'w':
                self.rm_wall(pos, (valid[0], valid[1]), 'west', 'east')
            pos = (valid[0], valid[1])
            self.corridors(pos)
            valid = self.neighbor(pos)

    def path_42(self):
        """
        Methode that make the 42 pattern
        """
        if self.x < 9 or self.y < 9:
            raise Path42Error('Invalid space for creating 42 pattern')
        st1 = int(self.x / 2 - 3)
        st2 = int(self.y / 2 - 2)
        for i in range(2):
            self.maze[st2 + i][st1].path_42 = True
        for i in range(3):
            self.maze[st2 + 2][st1 + i].path_42 = True
        for i in range(2):
            self.maze[st2 + 3 + i][st1 + 2].path_42 = True
        st1 += 4
        for i in range(2):
            self.maze[st2][st1 + i].path_42 = True
        for i in range(2):
            self.maze[st2 + i][st1 + 2].path_42 = True
        for i in range(2):
            self.maze[st2 + 2][st1 + 2 - i].path_42 = True
        for i in range(2):
            self.maze[st2 + 2 + i][st1].path_42 = True
        for i in range(3):
            self.maze[st2 + 4][st1 + i].path_42 = True
