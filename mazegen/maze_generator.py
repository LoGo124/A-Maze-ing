""" Recursive Backtracking """
import random
from time import sleep
from abc import ABC, abstractmethod

from .config import Config
from .maze import Maze, Cell
from .renerer import Renderer


class MazeGenerator(ABC):
    @abstractmethod
    def generate(conf: Config, renderer: Renderer = None) -> Maze: ...

    def solve_maze(maze: Maze, renderer: Renderer = None) -> str:
        """ BFS (Breadth-First Search) """
        queue: list[tuple[Cell, str]] = [(maze.entry, "")]
        maze.reset_visited()
        maze.entry.visited = True

        while queue:
            cell, path = queue.pop(0)
            if cell.is_exit:
                maze.set_path(path)
                if renderer:
                    renderer.reset_terminal()
                    renderer.render_maze(maze)
                    sleep(1/10)
                return path
            for dir, neighbor in cell.neighbors:
                if neighbor and not neighbor.visited and not cell.has_wall_on(dir):
                    neighbor.visited = True
                    queue.append((neighbor, path + dir))
                    if renderer:
                        maze.set_path(path)
                        renderer.reset_terminal()
                        renderer.render_maze(maze)
                        sleep(1/10)


class PerfectMazeGen(MazeGenerator):
    @staticmethod  # solo genera laberintos, no tiene info propia
    def generate(conf: Config, renderer: Renderer = None) -> Maze:
        random.seed(conf.seed)
        maze = Maze(conf.width,  conf.height, conf.entry, conf.exit)
        start_cell = maze.get_cell(*conf.entry)
        stack = []
        start_cell.visited = True
        stack.append(start_cell)
        while stack:
            current: Cell = stack[-1]
            unvisited = []
            for direction, neighbor in current.neighbors:
                if neighbor and not neighbor.visited:
                    unvisited.append((direction, neighbor))
            if unvisited:
                if renderer:
                    renderer.reset_terminal()
                    renderer.render_maze(maze)
                    sleep(1/45)
                direction, next_cell = random.choice(unvisited)
                maze.remove_wall(current, direction)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()
        return maze


class PacManMazeGen(MazeGenerator):
    @staticmethod
    def generate(conf: Config, renderer: Renderer = None) -> Maze:
        random.seed(conf.seed)
        maze = Maze(conf.width, conf.height, conf.entry, conf.exit)
        start_cell = maze.get_cell(*conf.entry)
        start_cell.visited = True
        frontier: list[tuple[Cell, str, Cell]] = []
        for direction, neighbor in start_cell.neighbors:
            if neighbor:
                frontier.append((start_cell, direction, neighbor))
        while frontier:
            current, direction, next_cell = random.choice(frontier)
            frontier.remove((current, direction, next_cell))
            if not next_cell.visited:
                if renderer:
                    renderer.reset_terminal()
                    renderer.render_maze(maze)
                    sleep(1/45)
                maze.remove_wall(current, direction)
                next_cell.visited = True
                for dir2, neighbor2 in next_cell.neighbors:
                    if neighbor2 and not neighbor2.visited:
                        frontier.append((next_cell, dir2, neighbor2))
        return maze
