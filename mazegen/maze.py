"""Definition of the Cell and Maze classes."""
import sys
from typing import List


class Cell:
    """Represent a single maze cell.

    Each cell knows its position, the walls surrounding it, its adjacent
    neighbors, and several status flags used by the maze generation and solver.

    Attributes:
        x (int): Column index of the cell in the maze.
        y (int): Row index of the cell in the maze.
        north (bool): True when the north wall exists.
        east (bool): True when the east wall exists.
        south (bool): True when the south wall exists.
        west (bool): True when the west wall exists.
        neighbor_n (Cell | None): Neighbor in the north direction.
        neighbor_e (Cell | None): Neighbor in the east direction.
        neighbor_s (Cell | None): Neighbor in the south direction.
        neighbor_w (Cell | None): Neighbor in the west direction.
        visited (bool): Indicates whether the cell has been visited.
        is_42 (bool): True when the cell belongs to the 42-pattern decoration.
        path (str): Direction string used to mark the next step in the path from this cell.
        is_entry (bool): True when the cell is the maze entry.
        is_exit (bool): True when the cell is the maze exit.
    """

    def __init__(
            self,
            x: int,
            y: int,
            hex_val: int = 15,
            visited: bool = False
            ):
        """Initialize a cell and its internal state.

        Args:
            x (int): Column index of the cell.
            y (int): Row index of the cell.
            hex_val (int, optional): Bitmask describing which walls are present.
                Defaults to 15, meaning all four walls are closed.
            visited (bool, optional): Whether the cell is marked as visited.
                Defaults to False.
        """
        # Coordinates
        self.x = x
        self.y = y

        # Walls
        self.north: bool = hex_val & 1 == 1
        self.east: bool = hex_val & 2 == 2
        self.south: bool = hex_val & 4 == 4
        self.west: bool = hex_val & 8 == 8

        # Neighbours
        self.neighbor_n: Cell | None = None
        self.neighbor_e: Cell | None = None
        self.neighbor_s: Cell | None = None
        self.neighbor_w: Cell | None = None

        # Other flags
        self.visited = visited
        self.is_42 = False
        self.path: str = ""
        self.is_entry: bool = False
        self.is_exit: bool = False

    @property
    def hex_val(self) -> int:
        """Return the wall bitmask for the cell.

        Returns:
            int: Value constructed from the north, east, south, and west wall flags.
        """
        return (
            (self.north * 1)
            + (self.east * 2)
            + (self.south * 4)
            + (self.west * 8)
            )

    @property
    def is_dead_end(self) -> bool:
        """Check whether the cell is a dead-end cell.

        Returns:
            bool: True if the cell has a dead-end wall pattern.
        """
        dead_end_values = [14, 13, 11, 7]
        return self.hex_val in dead_end_values

    @property
    def is_42_dead_end(self) -> bool:
        """Check whether the cell is a dead end adjacent to the 42 pattern.

        Returns:
            bool: True when the cell is a dead end and has 3 neighboring 42 cells.
        """
        surrounding_42_cells: int = 0
        for _, neighbor in self.neighbors:
            surrounding_42_cells += 1 if neighbor and neighbor.is_42 else 0
        return (surrounding_42_cells == 3 and self.is_dead_end)

    @property
    def is_closed(self) -> bool:
        """Check whether all walls are closed.

        Returns:
            bool: True when the cell is completely enclosed.
        """
        return (self.hex_val == 15)

    @property
    def is_path(self) -> bool:
        """Check whether the cell has a path mark.

        Returns:
            bool: True if the path string is not empty.
        """
        return (self.path is not None)

    @property
    def neighbors(self) -> List[tuple[str, "Cell | None"]]:
        """Return the direction/neighbor pairs for the cell.

        Returns:
            list[tuple[str, Cell | None]]: Neighbor list in N, E, S, W order.
                Missing borders are represented by None.
        """
        return [
            ("N", self.neighbor_n),
            ("E", self.neighbor_e),
            ("S", self.neighbor_s),
            ("W", self.neighbor_w)
            ]

    def __int__(self) -> int:
        """Convert the cell to its wall bitmask.

        Returns:
            int: The numeric representation of the wall mask.
        """
        return self.hex_val

    def __str__(self) -> str:
        """Return a one-character representation of the cell.

        Returns:
            str: The last and unique hexadecimal digit of the cell mask.
        """
        return (hex(int(self))[-1])

    def has_wall_on(self, direction: str) -> bool:
        """Check whether a wall exists on a given side.

        Args:
            direction (str): Direction to inspect: N, E, S, or W.

        Returns:
            bool: True if the wall is present for the requested direction.
        """
        if direction.upper() == "N":
            return self.north
        if direction.upper() == "S":
            return self.south
        if direction.upper() == "E":
            return self.east
        if direction.upper() == "W":
            return self.west
        return False

    def set_hex_val(self, hex_val: int = 15) -> None:
        """Update the cell wall configuration from a bitmask.

        Args:
            hex_val (int, optional): Bitmask representing the walls. Defaults to 15 (fully closed).
        """
        # Walls
        self.north = hex_val & 1 == 1
        self.east = hex_val & 2 == 2
        self.south = hex_val & 4 == 4
        self.west = hex_val & 8 == 8


class Maze:
    """Represent a maze board composed of Cell objects.

    The maze stores the grid, entry and exit cells, solution path information,
    warnings emitted during setup, and the 42-pattern decoration used by the
    project.

    Attributes:
        width (int): Number of columns in the maze.
        height (int): Number of rows in the maze.
        grid (list[list[Cell]]): Bidimensional maze structure.
        entry (Cell): Entrance cell of the maze.
        exit (Cell): Exit cell of the maze.
        path (str): Path string describing the solution route.
        warnings (list[Exception]): List of validation warnings.
    """

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            hex_grid: list[str] | None = None,
    ) -> None:
        """Initialize a maze.

        Args:
            width (int): Width of the maze in cells.
            height (int): Height of the maze in cells.
            entry (tuple[int, int]): Coordinates of the entry cell.
            exit (tuple[int, int]): Coordinates of the exit cell.
            hex_grid (list[str] | None, optional): Optional prebuilt maze grid in
                hexadecimal representation. Defaults to None.
        """
        self.width: int = width
        self.height: int = height
        self.grid: list[list[Cell]]
        if hex_grid:
            self.width = len(hex_grid[0])
            self.height = len(hex_grid)
            self.grid = [
                [Cell(x, y, int(hex_val, 16)) for x, hex_val in enumerate(row)]
                for y, row in enumerate(hex_grid)
            ]
        else:
            self.grid = [
                [Cell(x, y) for x in range(width)]
                for y in range(height)
            ]
        self.entry: Cell
        self.exit: Cell
        self.path: str = ""
        self.warnings: list[Exception] = []
        if entry == exit and isinstance(entry, tuple):
            self.warnings.append(
                ValueError(
                    "Entry and exit coordinates should be different,"
                    f"both values are set to: {entry}"
                )
            )
        self._set_pattern()
        self.set_entry(*entry) if entry else None
        self.set_exit(*exit) if exit else None
        self._bind_neighbors()

    def __str__(self) -> str:
        """Return a printable representation of the maze.

        Returns:
            str: Serialized maze data including grid, entry, exit, and path.
        """
        maze_str = ""
        for y in range(self.height):
            for x in range(self.width):
                maze_str += str(self.grid[y][x])
            maze_str += "\n"
        maze_str += "\n"
        maze_str += f"{self.entry.x},{self.entry.y}\n" if self.entry else ""
        maze_str += f"{self.exit.x},{self.exit.y}\n" if self.exit else ""
        maze_str += f"{self.path}\n" if self.path else ""
        return maze_str

    def __int__(self) -> int:
        """Return the total number of cells in the maze.

        Returns:
            int: The area of the maze as width * height.
        """
        return (self.height * self.width)

    def __iter__(self) -> "Maze":
        """Initialize iteration over all cells in row-major order.

        Returns:
            Maze: The maze instance configured for iteration.
        """
        self._i = 0
        return self

    def __next__(self) -> Cell:
        """Return the next cell during iteration.

        Returns:
            Cell: The next cell in the maze.

        Raises:
            StopIteration: When iteration reaches the end of the grid.
        """
        y = self._i // len(self.grid[0])
        x = self._i % len(self.grid[0])
        if x == 0 and y >= len(self.grid):
            raise StopIteration
        current_cell = self.grid[y][x]
        self._i += 1
        return current_cell

    def _clamp_coordinates(self, x: int, y: int) -> tuple[int, int]:
        """Clamp coordinates to the maze bounds.

        Args:
            x (int): Candidate x coordinate.
            y (int): Candidate y coordinate.

        Returns:
            tuple[int, int]: Corrected coordinates inside the maze bounds.
        """
        x = min(x, self.width - 1) if x > 0 else 0
        y = min(y, self.height - 1) if y > 0 else 0
        return (x, y)

    def _bind_neighbors(self) -> None:
        """Link each cell to its adjacent neighbors in all four directions."""
        for cell in self:
            cell.neighbor_n = self.get_cell(cell.x, cell.y - 1)
            cell.neighbor_e = self.get_cell(cell.x + 1, cell.y)
            cell.neighbor_s = self.get_cell(cell.x, cell.y + 1)
            cell.neighbor_w = self.get_cell(cell.x - 1, cell.y)

    def _set_pattern(self) -> None:
        """Apply the 42 decorative pattern to the maze cells when possible."""
        PATTERN_42: list[list[int]] = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        if self.width < 9 or self.height < 7:
            self.warnings.append(
                ValueError("Maze is too small to fit the '42' pattern.")
                )
            return

        start_x, start_y = ((self.width - 9) // 2), ((self.height - 7) // 2)

        for (py, y) in enumerate(range(start_y, start_y + 7)):
            for (px, x) in enumerate(range(start_x, start_x + 9)):
                self.grid[y][x].is_42 = bool(PATTERN_42[py][px])
                self.grid[y][x].visited = bool(PATTERN_42[py][px])
        return

    def save(self, path: str) -> None:
        """Persist the maze to disk.

        Args:
            path (str): Destination file path.
        """
        try:
            with open(path, "w") as f:
                f.write(str(self))
            for warn in self.warnings:
                if isinstance(warn, PermissionError) and warn.filename == path:
                    self.warnings.remove(warn)
        except Exception as e:
            self.warnings.append(e)

    @staticmethod
    def load(path: str) -> "Maze":
        """Load a maze from a serialized file.

        Args:
            path (str): Path to the serialized maze file.

        Returns:
            Maze: The reconstructed maze object.

        Raises:
            SystemExit: If the file cannot be read or the content is invalid.
        """
        try:
            with open(path, "r") as f:
                hex_grid = []
                line = f.readline()
                while (line != "\n"):
                    hex_grid.append(line[0:-1])
                    line = f.readline()
                line = f.readline()
                line = line[0:-1]
                coord: tuple[int, ...] = tuple(map(int, line.split(",")))
                entry: tuple[int, int] = (coord[0], coord[1])
                line = f.readline()
                line = line[0:-1]
                coord = tuple(map(int, line.split(",")))
                exit: tuple[int, int] = (coord[0], coord[1])
                line = f.readline()
                exit_path = line[0:-1]
            maze = Maze(
                len(hex_grid[0]),
                len(hex_grid),
                entry,
                exit,
                hex_grid=hex_grid
            )
            maze.set_path(exit_path)
            return maze
        except OSError as e:
            sys.exit(e.strerror)
        except Exception as e:
            sys.exit(e.args[0])

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Return the cell at the given coordinates if it exists.

        Args:
            x (int): X coordinate of the cell.
            y (int): Y coordinate of the cell.

        Returns:
            Cell | None: The requested cell or None when out of bounds.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def get_neighbors(self, cell: Cell) -> list[tuple[str, Cell | None]]:
        """Return all direction/neighbor pairs for a cell.

        Args:
            cell (Cell): The cell whose neighbors will be returned.

        Returns:
            list[tuple[str, Cell | None]]: Neighbor pairs in N, E, S, W order.
        """
        return cell.neighbors

    def set_entry(self, x: int, y: int) -> None:
        """Set the maze entry cell.

        Args:
            x (int): X coordinate for the entry cell.
            y (int): Y coordinate for the entry cell.
        """
        if (x, y) != self._clamp_coordinates(x, y):
            self.warnings.append(
                ValueError(
                    f"Entry cell coordinates ({x}, {y}), are out of bounds. "
                    f"They have been corrected to "
                    f"{self._clamp_coordinates(x, y)}."
                )
            )
            x, y = self._clamp_coordinates(x, y)
        cell = self.get_cell(x, y)
        if cell and cell.is_42:
            cell.is_42 = False
            cell.visited = False
            self.warnings.append(
                ValueError(
                    f"Entry cell ({x}, {y}) is part of the '42' pattern. "
                    "This will break the pattern and may cause issues in "
                    "the maze generation process."
                )
            )
        if cell:
            cell.is_entry = True
            self.entry = cell

    def set_exit(self, x: int, y: int) -> None:
        """Set the maze exit cell.

        Args:
            x (int): X coordinate for the exit cell.
            y (int): Y coordinate for the exit cell.
        """
        if (x, y) != self._clamp_coordinates(x, y):
            self.warnings.append(
                ValueError(f"Exit cell coordinates ({x}, {y}), "
                           f"are out of bounds. They have been corrected to "
                           f"{self._clamp_coordinates(x, y)}.")
                )
            x, y = self._clamp_coordinates(x, y)
        cell = self.get_cell(x, y)
        if cell and cell.is_42:
            cell.is_42 = False
            cell.visited = False
            self.warnings.append(
                ValueError(f"Exit cell ({x}, {y}) is part of the '42' pattern."
                           " This will break the pattern and may cause issues"
                           " in the maze generation process.")
                )
        if cell == self.entry:
            self.warnings.append(
                ValueError(f"Exit cell ({x}, {y}) is the same as the entry"
                           " cell. This implies that the maze solution path "
                           "is \"\" There is no cell with is_path set to True")
                )
        if cell:
            cell.is_exit = True
            self.exit = cell

    def set_path(self, path: str) -> None:
        """Apply a path string across the maze from the entry cell.

        Args:
            path (str): Sequence of movement directions such as N, E, S, or W.
        """
        self.reset_path()
        self.path = path
        coordinates = (self.entry.x, self.entry.y)
        for direction in path:
            cell = self.get_cell(coordinates[0], coordinates[1])
            if cell:
                cell.path = direction
                if direction == "N":
                    coordinates = (coordinates[0], coordinates[1] - 1)
                elif direction == "E":
                    coordinates = (coordinates[0] + 1, coordinates[1])
                elif direction == "S":
                    coordinates = (coordinates[0], coordinates[1] + 1)
                elif direction == "W":
                    coordinates = (coordinates[0] - 1, coordinates[1])

    def remove_wall(self, current: Cell, direction: str) -> None:
        """Remove the wall between a cell and the adjacent one in a direction.

        Args:
            current (Cell): Current cell whose wall is to be removed.
            direction (str): Direction of the adjacent cell: N, E, S, or W.
        """
        if direction == "N" and current.neighbor_n:
            current.north = False
            current.neighbor_n.south = False
        elif direction == "E" and current.neighbor_e:
            current.east = False
            current.neighbor_e.west = False
        elif direction == "S" and current.neighbor_s:
            current.south = False
            current.neighbor_s.north = False
        elif direction == "W" and current.neighbor_w:
            current.west = False
            current.neighbor_w.east = False

    def reset_visited(self) -> None:
        """Clear the visited flags for every cell in the maze."""
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def reset_path(self) -> None:
        """Clear the path data stored on every cell and the maze itself."""
        self.path = ""
        for row in self.grid:
            for cell in row:
                cell.path = ""
