import random

from .maze import Maze, Cell


class MazeGenerator():
    def __init__(self, width: int, height: int, entry: tuple[int], exit: tuple[int], perfect: bool, seed: int = 42):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed

    def generate(self) -> Maze:
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

    def _generate_backtracking(self) -> Maze:
        random.seed(self.seed)
        maze = Maze(self.width,  self.height, self.entry, self.exit)
        start_cell = maze.get_cell(*self.entry)
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

    def _generate_prim(self) -> Maze:
        random.seed(self.seed)
        maze = Maze(self.width, self.height, self.entry, self.exit)
        start_cell = maze.get_cell(*self.entry)
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

    def solve_maze(self, maze: Maze) -> Maze:
        """ BFS (Breadth-First Search) """
        queue: list[tuple[Cell, str]] = [(maze.entry, "")]
        maze.reset_visited()
        maze.entry.visited = True

        while queue:
            cell, path = queue.pop(0)
            if cell.is_exit:
                maze.set_path(path)
                return
            for dir, neighbor in cell.neighbors:
                if neighbor and not neighbor.visited and not cell.has_wall_on(dir):
                    neighbor.visited = True
                    queue.append((neighbor, path + dir))
                    maze.set_path(path + dir)
                    yield maze

    def handle_dead_ends(self, maze: Maze) -> Maze:
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
                for dir, neighbour in cell.neighbors:
                    if neighbour and not neighbour.is_42 and cell.has_wall_on(dir):
                        maze.remove_wall(cell, dir)
                        yield maze
                        break
        return
