""" Recursive Backtracking """
import random
from typing import List
from maze import Maze, Cell
from config import Config


class MazeGenerator:
    @staticmethod  # solo genera laberintos, no tiene info propia
    def generate_perfect(conf: Config) -> Maze:
        random.seed(conf.seed)
        maze = Maze(5,  5)
        start_cell = maze.get_cell(conf.entry[0], conf.entry[1])
        stack = []
        start_cell.visited = True
        stack.append(start_cell)
        while stack:
            current = stack[-1]
            neighbors = maze.get_neighbors(current)
            unvisited = []
            for direction, neighbor in neighbors:
                if not neighbor.visited:
                    unvisited.append((direction, neighbor))
            if unvisited:
                direction, next_cell = random.choice(unvisited)
                maze.remove_wall(current, direction)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()
        return maze
