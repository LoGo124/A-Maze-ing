"""definition of the Cell and Maze classes"""
from typing import overload

HEX_CELL_TO_ANSI = {
                0: "\033[38;5;91m██\033[0m",
                1: "\033[38;5;54m██\033[0m",
                2: "\033[38;5;34m██\033[0m",
                3: "\033[38;5;91m██\033[0m",
                4: "\033[38;5;92m██\033[0m",
                5: "\033[38;5;54m██\033[0m",
                6: "\033[38;5;54m██\033[0m",
                7: "\033[38;5;34m██\033[0m",
                8: "\033[38;5;91m██\033[0m",
                9: "\033[38;5;92m██\033[0m",
                10: "\033[38;5;54m██\033[0m",
                11: "\033[38;5;54m██\033[0m",
                12: "\033[38;5;34m██\033[0m",
                13: "\033[38;5;54m██\033[0m",
                14: "\033[38;5;91m██\033[0m",
                15: "\033[38;5;92m██\033[0m",
            }

HEX_MAZE_8X8 = (
        "93359336",
        "C96C8324",
        "36A5824C",
        "C05934C3",
        "9516A5A3",
        "A36AC24C",
        "9024C926",
        "A336C336"
    )


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
        self.is_path = False

    @property
    def hex_cell(self) -> int:
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
    def neighbors(self):
        return [
            ("N", self.neighbor_n),
            ("E", self.neighbor_e),
            ("S", self.neighbor_s),
            ("W", self.neighbor_w)
            ]


class Maze():
    @overload
    def __init__(self, width: int, height: int) -> None:
        ...

    @overload
    def __init__(self, hex_grid: tuple) -> None:
        ...

    def __init__(self, width: int = None, height: int = None, hex_grid: tuple = None) -> None:
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
                for y in range(height)
                ]
                for x in range(width)
            ]
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
        return maze_str

    def __int__(self) -> int:
        return (self.height * self.width)

    def get_cell(self, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def get_neighbors(self, cell: Cell) -> list[tuple[str, Cell]]:
        return cell.neighbors

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
