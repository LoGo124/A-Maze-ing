from collections.abc import Iterable
import random

from .maze import Maze, Cell


class MazeGenerator:
    """Generate and solve mazes with configurable generation strategies.

    The generator can create either a perfect maze or a maze with loops and then
    solve it via breadth-first search. It also provides a dead-end handling step
    used by the non-perfect generator.

    Attributes:
        width (int): Number of columns in the maze.
        height (int): Number of rows in the maze.
        entry (tuple[int, int]): Coordinates of the maze entry cell.
        exit (tuple[int, int]): Coordinates of the maze exit cell.
        perfect (bool): If True, generate a perfect maze without loops.
        seed (int): Random seed used by the generator.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: int | None = None
    ) -> None:
        """Initialize the maze generator with the generation parameters.

        Args:
            width: Number of columns.
            height: Number of rows.
            entry: (x, y) coordinates of the entry cell.
            exit: (x, y) coordinates of the exit cell.
            perfect: If True, build a spanning tree (no loops).
            seed: Base seed; 42 is used when None.
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = 42 if not seed else seed

    def generate(self) -> Iterable[Maze]:
        """Generate and solve a maze, yielding the maze after each step.

        The internal seed is incremented on each call so consecutive calls produce
        different but reproducible mazes.

        Yields:
            Maze: A maze state after each generation or solving step. The final
            yielded maze is the solved configuration.
        """
        self.seed += 1
        if self.perfect:
            for maze in self._generate_backtracking():
                yield maze
            for maze in self.solve_maze(maze):
                yield maze
        else:
            for maze in self._generate_prim():
                yield maze
            for maze in self.handle_dead_ends(maze):
                yield maze
            for maze in self.solve_maze(maze):
                yield maze
        return

    def _generate_backtracking(self) -> Iterable[Maze]:
        """Generate a perfect maze using iterative depth-first backtracking.

        This method walks the maze from the entry cell using a stack, carving
        walls between connected cells and yielding each intermediate maze state.

        Yields:
            Maze: The maze after each removed wall during carving.
        """
        random.seed(self.seed)
        maze = Maze(self.width, self.height, self.entry, self.exit)
        start_cell = maze.entry
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
                direction, next_cell = random.choice(unvisited)
                maze.remove_wall(current, direction)
                next_cell.visited = True
                stack.append(next_cell)
                yield maze
            else:
                stack.pop()
        return

    def _generate_prim(self) -> Iterable[Maze]:
        """Generate a maze with randomized Prim's algorithm.

        The frontier-based method expands from the entry cell, adding walls to a
        frontier and carving random connections until the whole maze is connected.

        Yields:
            Maze: The maze after each wall removal during frontier expansion.
        """
        random.seed(self.seed)
        maze = Maze(self.width, self.height, self.entry, self.exit)
        start_cell = maze.entry
        start_cell.visited = True
        frontier: list[tuple[Cell, str, Cell]] = []
        for direction, neighbor in start_cell.neighbors:
            if neighbor:
                frontier.append((start_cell, direction, neighbor))
        while frontier:
            current, direction, next_cell = random.choice(frontier)
            frontier.remove((current, direction, next_cell))
            if not next_cell.visited:
                maze.remove_wall(current, direction)
                next_cell.visited = True
                yield maze
                for dir2, neighbor2 in next_cell.neighbors:
                    if neighbor2 and not neighbor2.visited:
                        frontier.append((next_cell, dir2, neighbor2))
        return

    def solve_maze(self, maze: Maze) -> Iterable[Maze]:
        """It uses BFS (Breadth-First Search) to find the shortest path
        Args:
            maze (Maze): The maze to solve.

        Yields:
            Maze: Intermediate maze states showing the explored path as the
            algorithm advances toward the exit.
        """
        queue: list[tuple[Cell, str]] = [(maze.entry, "")]
        maze.reset_visited()
        maze.entry.visited = True

        while queue:
            cell, path = queue.pop(0)
            if cell.is_exit:
                maze.set_path(path)
                return
            for dir, n in cell.neighbors:
                if n and not n.visited and not cell.has_wall_on(dir):
                    n.visited = True
                    queue.append((n, path + dir))
                    maze.set_path(path + dir)
                    yield maze

    def handle_dead_ends(self, maze: Maze) -> Iterable[Maze]:
        """Remove dead ends from a maze until no such cells remain.

        The method iterates over dead-end cells and removes walls in a way that
        keeps the structure compatible with the 42-pattern rules.

        Args:
            maze (Maze): Maze instance whose dead ends will be processed.

        Yields:
            Maze: The maze after each dead-end wall removal.
        """
        dead_end_cells = [cell for cell in maze if cell.is_dead_end]
        for cell in dead_end_cells:
            while cell.is_dead_end and not cell.is_42_dead_end:
                for dir, neighbour in cell.neighbors:
                    if neighbour and neighbour.is_dead_end:
                        maze.remove_wall(cell, dir)
                        yield maze
                        break
                if not cell.is_dead_end:
                    continue
                for dir, n in cell.neighbors:
                    if n and not n.is_42 and cell.has_wall_on(dir):
                        maze.remove_wall(cell, dir)
                        yield maze
                        break
        return
