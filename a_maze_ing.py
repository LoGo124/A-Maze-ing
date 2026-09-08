"""Módulo principal del proyecto A-ma-zing."""
import sys
from enum import Enum

HEX_CELL_TO_ASCII = {
                0 : "0",
                1 : "1",
                2 : "2",
                3 : "3",
                4 : "4",
                5 : "5",
                6 : "6",
                7 : "7",
                8 : "8",
                9 : "9",
                10 : "a",
                11 : "b",
                12 : "c",
                13 : "d",
                14 : "e",
                15 : "f",
            }

ASCII_TO_HEX_CELL = {v: k for k, v in HEX_CELL_TO_ASCII.items()}

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


class Terminal(str, Enum):
    """Secuencias de escape ANSI para el control de la terminal."""

    ALT_SCREEN_ON = "\033[?1049h"
    ALT_SCREEN_OFF = "\033[?1049l"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    CLEAR = "\033[2J"
    HOME = "\033[H"
    RESET = "\033[0m"
    WALL_STYLE = "\033[44m  \033[0m"  # Bloque azul para pared
    PATH_STYLE = "  "                 # Espacio vacío para camino
    PLAYER_STYLE = "\033[1;32mP \033[0m"  # 'P' verde brillante


class Cell():
    def __init__(self, hex_cell):
        self.west: bool = hex_cell // 8 == 1
        hex_cell -= 8 if self.west else 0
        self.south: bool = hex_cell // 4 == 1
        hex_cell -= 4 if self.south else 0
        self.east: bool = hex_cell // 2 == 1
        hex_cell -= 2 if self.east else 0
        self.north: bool = hex_cell // 1 == 1

    @property
    def hex_cell(self) -> int:
        return ((self.west * 8) + (self.south * 4) + (self.east * 2) + (self.north * 1))

    def __str__(self):
        return (HEX_CELL_TO_ASCII[self.hex_cell])

    @property
    def is_closed(self):
        return (self.hex_cell == 15)


class MazeGenerator:
    """Representa la estructura interna y estado del laberinto.

    Attributes:
        grid (list[list[int]]): Matriz 2D donde 1 representa pared y 0 camino.
    """
    def load_grid(grid: tuple[str]) -> list[list[Cell]]:
        maze: list[list[Cell]] = []
        raw_i = 0
        for raw in grid:
            maze.append([])
            for col in raw:
                maze[raw_i].append(Cell(ASCII_TO_HEX_CELL[col.lower()]))
                print(maze[raw_i][-1], end="")
            raw_i += 1
            print()
        return maze

    def gen_maze(config: Config) -> Maze:
        pass


class MazeRenderer:
    """Encapsula el dibujado visual del laberinto en la consola."""

    TILE_MAP = {
        1: Terminal.WALL_STYLE,
        0: Terminal.PATH_STYLE,
        2: Terminal.PLAYER_STYLE,
    }

    def render(self, maze: MazeGenerator) -> str:
        """Genera la representación completa del laberinto como una cadena.

        Args:
            maze (Maze): Instancia del laberinto a renderizar.

        Returns:
            str: Mapa listo para imprimirse con colores ANSI.
        """
        lines = [
            "".join(self.TILE_MAP.get(cell, "??") for cell in row)
            for row in maze.grid
        ]
        return "\n".join(lines)


def run() -> None:
    """Ejecuta el ciclo de vida de la aplicación."""

    maze: list[list[Cell]] = MazeGenerator.load_grid(grid=HEX_MAZE_8X8)

    renderer = MazeRenderer()

    # Activa la pantalla secundaria y oculta el cursor
    sys.stdout.write(f"{Terminal.ALT_SCREEN_ON}{Terminal.HIDE_CURSOR}{Terminal.CLEAR}")
    sys.stdout.flush()

    try:
        # Dibuja el laberinto llevando el cursor al inicio
        sys.stdout.write(f"{Terminal.HOME}{renderer.render(maze)}\n")
        sys.stdout.flush()

        # Pausa para ver el resultado antes de salir
        input("\nPresiona [Enter] para salir...")

    finally:
        # Se ejecuta SIEMPRE para restaurar la terminal del usuario
        sys.stdout.write(f"{Terminal.SHOW_CURSOR}{Terminal.ALT_SCREEN_OFF}")
        sys.stdout.flush()


if __name__ == "__main__":
    run()
