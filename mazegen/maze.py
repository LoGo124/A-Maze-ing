"""definition of the Cell and Maze classes"""
from typing import overload, Any
from sys import stderr


class Cell():
    def __init__(
            self,
            x: int,
            y: int,
            hex_val: int = 15,
            visited: bool = False
            ):
        # Coordinates
        self.x = x
        self.y = y

        # Walls
        self.north: bool = hex_val & 1 == 1
        self.east: bool = hex_val & 2 == 2
        self.south: bool = hex_val & 4 == 4
        self.west: bool = hex_val & 8 == 8

        # Neighbours
        self.neighbor_n: Cell = None
        self.neighbor_e: Cell = None
        self.neighbor_s: Cell = None
        self.neighbor_w: Cell = None

        # Other flags
        self.visited = visited
        self.is_42 = False
        self.path: str = ""
        self.is_entry: bool = False
        self.is_exit: bool = False

    @property
    def hex_val(self) -> int:
        """AI is creating summary for hex_val

        Returns:
            int: [description]
        """
        return (
            (self.north * 1)
            + (self.east * 2)
            + (self.south * 4)
            + (self.west * 8)
            )

    @property
    def is_dead_end(self):
        dead_end_values = [14, 13, 11, 7]
        return self.hex_val in dead_end_values

    @property
    def is_42_dead_end(self) -> bool:
        surrounding_42_cells: int = 0
        for _, neighbor in self.neighbors:
            surrounding_42_cells += 1 if neighbor and neighbor.is_42 else 0
        return (surrounding_42_cells == 3 and self.is_dead_end)

    @property
    def is_closed(self):
        return (self.hex_val == 15)

    @property
    def is_path(self):
        return (self.path is not None)

    @property
    def neighbors(self) -> tuple[str, Any]:
        return [
            ("N", self.neighbor_n),
            ("E", self.neighbor_e),
            ("S", self.neighbor_s),
            ("W", self.neighbor_w)
            ]

    def __int__(self):
        return self.hex_val

    def __hex__(self):
        return f"{hex(self.hex_val)}"

    def __str__(self):
        return (hex(int(self))[-1])

    def has_wall_on(self, direction: str):
        if direction.upper() == "N":
            return self.north
        if direction.upper() == "S":
            return self.south
        if direction.upper() == "E":
            return self.east
        if direction.upper() == "W":
            return self.west

    def set_hex_val(self, hex_val: int = 15):
        # Walls
        self.north: bool = hex_val & 1 == 1
        self.east: bool = hex_val & 2 == 2
        self.south: bool = hex_val & 4 == 4
        self.west: bool = hex_val & 8 == 8


class Maze():

    @overload
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int],
        exit: tuple[int]
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        hex_grid: tuple,
        entry: tuple[int, int],
        exit: tuple[int, int]
    ) -> None:
        ...

    def __init__(
            self,
            width: int = None,
            height: int = None,
            entry: tuple[int] = None,
            exit: tuple[int] = None,
            hex_grid: tuple = None
    ) -> None:
        if hex_grid is not None:
            self.width: int = len(hex_grid[0])
            self.height: int = len(hex_grid)
            self.grid: list[list[Cell]] = [[
                Cell(x, y, int(hex_val, 16))
                for x, hex_val in enumerate(row)
                ]
                for y, row in enumerate(hex_grid)
                ]
        else:
            self.width: int = width
            self.height: int = height
            self.grid: list[list[Cell]] = [[
                Cell(x, y)
                for x in range(width)
                ]
                for y in range(height)
            ]
        self.entry: Cell = None
        self.exit: Cell = None
        self.path: list[str] = None
        self.warnings: list[Exception] = []
        if entry == exit and isinstance(entry, tuple):
            self.warnings.append(ValueError(f"Entry and exit coordinates should be different, both values are set to: {entry}"))
        self._set_pattern()
        self.set_entry(*entry) if entry else None
        self.set_exit(*exit) if exit else None
        self._bind_neighbors()

    def __str__(self) -> str:
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
        return (self.height * self.width)

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self) -> Cell:
        y = self._i // len(self.grid[0])
        x = self._i % len(self.grid[0])
        if x == 0 and y >= len(self.grid):
            raise StopIteration
        current_cell = self.grid[y][x]
        self._i += 1
        return current_cell

    def _coordinate_correction(self, x: int, y: int) -> tuple[int, int]:
        x = min(x, self.width - 1) if x > 0 else 0
        y = min(y, self.height - 1) if y > 0 else 0
        return (x, y)

    def _bind_neighbors(self) -> None:
        for row in self.grid:
            for cell in row:
                cell.neighbor_n = self.get_cell(cell.x, cell.y - 1)
                cell.neighbor_e = self.get_cell(cell.x + 1, cell.y)
                cell.neighbor_s = self.get_cell(cell.x, cell.y + 1)
                cell.neighbor_w = self.get_cell(cell.x - 1, cell.y)

    def _set_pattern(self) -> None:
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
        try:
            with open(path, "w") as f:
                f.write(str(self))
        except Exception as e:
            self.warnings.append(e)

    @staticmethod
    def load(path: str):  # -> Maze:
        try:
            with open(path, "r") as f:
                hex_grid = []
                line = f.readline()
                while (line != "\n"):
                    hex_grid.append(line[0:-1])
                    line = f.readline()
                line = f.readline()
                line = line[0:-1]
                entry = (int(val) for val in line.split(","))
                line = f.readline()
                line = line[0:-1]
                exit = (int(val) for val in line.split(","))
                line = f.readline()
                exit_path = line[0:-1]
            maze = Maze(hex_grid=hex_grid, entry=entry, exit=exit)
            maze.set_path(exit_path)
            return maze
        except OSError as e:
            stderr.write(e)
        except Exception as e:
            stderr.write(e)
            raise Exception

    def get_cell(self, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def get_neighbors(self, cell: Cell) -> list[tuple[str, Cell]]:
        return cell.neighbors

    def set_entry(self, x: int, y: int) -> None:
        if (x, y) != self._coordinate_correction(x, y):
            self.warnings.append(
                ValueError(f"Entry cell coordinates ({x}, {y}), are out of bounds. They have been corrected to {self._coordinate_correction(x, y)}.")
                )
            x, y = self._coordinate_correction(x, y)
        cell = self.get_cell(x, y)
        if cell.is_42:
            cell.is_42 = False
            cell.visited = False
            self.warnings.append(
                ValueError(f"Entry cell ({x}, {y}) is part of the '42' pattern. This will break the pattern and may cause issues in the maze generation process.")
                )
        if cell:
            cell.is_entry = True
            self.entry = cell

    def set_exit(self, x: int, y: int) -> None:
        if (x, y) != self._coordinate_correction(x, y):
            self.warnings.append(
                ValueError(f"Exit cell coordinates ({x}, {y}), are out of bounds. They have been corrected to {self._coordinate_correction(x, y)}.")
                )
            x, y = self._coordinate_correction(x, y)
        cell = self.get_cell(x, y)
        if cell.is_42:
            cell.is_42 = False
            cell.visited = False
            self.warnings.append(
                ValueError(f"Exit cell ({x}, {y}) is part of the '42' pattern. This will break the pattern and may cause issues in the maze generation process.")
                )
        if cell == self.entry:
            self.warnings.append(
                ValueError(f"Exit cell ({x}, {y}) is the same as the entry cell. This implies that the maze solution path is \"\" and there is no cell with is_path set to True.")
                )
        if cell:
            cell.is_exit = True
            self.exit = cell

    def set_path(self, path: str) -> None:
        self.reset_path()
        self.path = path
        coordinates = (self.entry.x, self.entry.y)
        for direction in path:
            cell = self.get_cell(coordinates[0], coordinates[1])
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
        if direction == "N":
            current.north = False
            current.neighbor_n.south = False
        elif direction == "E":
            current.east = False
            current.neighbor_e.west = False
        elif direction == "S":
            current.south = False
            current.neighbor_s.north = False
        elif direction == "W":
            current.west = False
            current.neighbor_w.east = False

    def reset_visited(self) -> None:
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def reset_path(self) -> None:
        self.path = None
        for row in self.grid:
            for cell in row:
                cell.path = None
