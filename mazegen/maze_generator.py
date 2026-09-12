""" Recursive Backtracking """
import random
from time import sleep

from .config import Config
from .maze import Maze
from .renerer import Renderer


class MazeGenerator:
    @staticmethod  # solo genera laberintos, no tiene info propia
    def generate_perfect(conf: Config, renderer: Renderer = None) -> Maze:
        random.seed(conf.seed)
        maze = Maze(conf.width,  conf.height, conf.entry, conf.exit)
        start_cell = maze.get_cell(*conf.entry)
        stack = []
        start_cell.visited = True
        stack.append(start_cell)
        while stack:
            current = stack[-1]
            neighbors = maze.get_neighbors(current)
            unvisited = []
            for direction, neighbor in neighbors:
                if neighbor and not neighbor.visited:
                    unvisited.append((direction, neighbor))
            if unvisited:
                if renderer:
                    renderer.reset_terminal()
                    renderer.render_maze(maze)
                    sleep(1/60)
                direction, next_cell = random.choice(unvisited)
                maze.remove_wall(current, direction)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()
        return maze
