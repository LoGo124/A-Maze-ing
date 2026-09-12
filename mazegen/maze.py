"""definition of the Cell and Maze classes"""
from typing import overload


class Cell():
    def __init__(
            self,
            x: int,
            y: int,
            hex_cell: int = 15,
            visited: bool = False
            ):
        # Coordinates
        self.x = x
        self.y = y

        # Walls
        self.north: bool = hex_cell & 1 == 1
        self.east: bool = hex_cell & 2 == 2
        self.south: bool = hex_cell & 4 == 4
        self.west: bool = hex_cell & 8 == 8

        # Neighbours
        self.neighbor_n: Cell = None
        self.neighbor_e: Cell = None
        self.neighbor_s: Cell = None
        self.neighbor_w: Cell = None

        # Other flags
        self.visited = visited
        self.is_42_pattern = False
        self.path: str | None = None
        self.is_entry: bool = False
        self.is_exit: bool = False

    @property
    def hex_cell(self) -> int:
        """AI is creating summary for hex_cell

        Returns:
            int: [description]
        """
        return (
            (self.north * 1)
            + (self.east * 2)
            + (self.south * 4)
            + (self.west * 8)
            )

    def __int__(self):
        return self.hex_cell

    def __hex__(self):
        return f"{self.hex_cell:x}"

    def __str__(self):
        return (hex(int(self))[-1])

    @property
    def is_closed(self):
        return (self.hex_cell == 15)

    @property
    def is_path(self):
        return (self.path is not None)

    @property
    def neighbors(self):
        return [
            ("N", self.neighbor_n),
            ("E", self.neighbor_e),
            ("S", self.neighbor_s),
            ("W", self.neighbor_w)
            ]


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
                Cell(x, y, int(hex_cell, 16))
                for x, hex_cell in enumerate(row)
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
        self.path: list[str] = None
        self.set_entry(*entry) if entry else None
        self.set_exit(*exit) if exit else None
        self._bind_neighbors()

    def _bind_neighbors(self) -> None:
        for row in self.grid:
            for cell in row:
                cell.neighbor_n = self.get_cell(cell.x, cell.y - 1)
                cell.neighbor_e = self.get_cell(cell.x + 1, cell.y)
                cell.neighbor_s = self.get_cell(cell.x, cell.y + 1)
                cell.neighbor_w = self.get_cell(cell.x - 1, cell.y)

    def __str__(self) -> str:
        maze_str = ""
        for y in range(self.height):
            for x in range(self.width):
                maze_str += str(self.grid[y][x])
            maze_str += "\n"
        maze_str += "\n"
        maze_str += f"{self.entry[0]},{self.entry[1]}\n" if self.entry else ""
        maze_str += f"{self.exit[0]},{self.exit[1]}\n" if self.exit else ""
        maze_str += f"{self.path}\n" if self.path else ""
        return maze_str

    def __int__(self) -> int:
        return (self.height * self.width)

    def save(self, path: str) -> None:
        try:
            with open(path, "w") as f:
                f.write(str(self))
        except OSError as e:
            print(e)
        except Exception as e:
            print(e)

    def load(path: str) -> Maze:
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
            print(e)
        except Exception as e:
            print(e)
            raise Exception

    def get_cell(self, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def get_neighbors(self, cell: Cell) -> list[tuple[str, Cell]]:
        return cell.neighbors

    def set_entry(self, x: int, y: int) -> None:
        cell = self.get_cell(x, y)
        if cell:
            cell.is_entry = True
            self.entry = (x, y)

    def set_exit(self, x: int, y: int) -> None:
        cell = self.get_cell(x, y)
        if cell:
            cell.is_exit = True
            self.exit = (x, y)

    def set_path(self, path: str) -> None:
        self.path = path
        coordinates = self.entry
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
        for col in self.grid:
            for cell in col:
                cell.visited = False
