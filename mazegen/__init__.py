"""Generate and solve mazes as reusable library code.

Example:
    >>> from mazegen import MazeGenerator
    >>> generator = MazeGenerator(21, 15, (0, 0), (20, 14), True, seed=42)
    >>> frames = list(generator.generate())
    >>> maze = frames[-1]
    >>> maze.path is not None
    True
"""

from .maze import Maze, Cell
from .maze_generator import MazeGenerator

__all__ = ["Maze", "Cell", "MazeGenerator"]
