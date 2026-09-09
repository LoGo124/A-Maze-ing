""" Recursive Backtracking """

import random
from typing import List
from maze import Maze, Cell


class MazeGenerator:
    @staticmethod  # solo genera laberintos, no tiene info propia
    def generate_perfect(start_xy: tuple[int, int] = (0, 0), seed: int = 42) -> Maze:
        random.seed(seed)
        maze = Maze(5,  5)
        start_cell = maze.get_cell(start_xy[0], start_xy[1])
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


def run() -> None:
    print(MazeGenerator.generate_perfect())
    


if __name__ == "__main__":
    run()
