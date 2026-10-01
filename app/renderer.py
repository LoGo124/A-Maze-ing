from typing import List
from sys import stderr

from mazegen import Maze, Cell


class Renderer:
    def __init__(self, config: dict = {}):
        self.config = config
        self.color_palettes: List[dict] = [
            {
                "bg": "\033[38;5;0m",  # Black background
                "wall": "\033[38;5;7m",  # White walls
                "entry": "\033[38;5;2m",  # Green entry
                "exit": "\033[38;5;1m",  # Red exit
                "path": "\033[38;5;215m",
                "42_pattern": "\033[38;5;213m"
            },
            {
                "bg": "\033[38;5;8m",  # Black background
                "wall": "\033[38;5;15m",  # White walls
                "entry": "\033[38;5;10m",  # Green entry
                "exit": "\033[38;5;9m",  # Red exit
                "path": "\033[38;5;11m",  # Yellow path
                "42_pattern": "\033[38;5;213m"
            },
            {
                "bg": "\033[38;5;235m",  # Black background
                "wall": "\033[38;5;16m",  # White walls
                "entry": "\033[38;5;51m",  # Green entry
                "exit": "\033[38;5;198m",  # Red exit
                "path": "\033[38;5;82m",  # Yellow path
                "42_pattern": "\033[38;5;99m"
            },
            {
                "bg": "\033[38;5;15m",
                "wall": "\033[38;5;235m",
                "entry": "\033[38;5;2m",
                "exit": "\033[38;5;2m",
                "path": "\033[106;5;30m",
                "42_pattern": "\033[38;5;2m"
            },
            {
                "bg": "\033[38;5;16m",        # Black background
                "wall": "\033[38;5;21m",      # Blue walls
                "entry": "\033[38;5;46m",     # Green entry
                "exit": "\033[38;5;196m",     # Red exit
                "path": "\033[38;5;226m",     # Yellow path
                "42_pattern": "\033[38;5;201m"  # Magenta/Pink pattern
            }

        ]
        self.color_palette: dict = self.color_palettes[0]

    def conmutate_color_palette(self) -> None:
        current_index = self.color_palettes.index(self.color_palette)
        next_index = (current_index + 1) % len(self.color_palettes)
        self.color_palette = self.color_palettes[next_index]

    def reset_terminal(self) -> None:
        print("\033[2J\033[H", end="")

    def render_menu(self) -> None:
        title = "="*5 + "A-maze-ing" + "="*5
        entries = [
            "\t1.\tGenerate maze",
            "\t2.\tShow the shortest path",
            "\t3.\tChange colors",
            "\t4.\tToggle animation",
            "\t8.\tSave maze",
            "\t9.\tLoad maze",
            "\t0.\tExit",
        ]
        print(title)
        print("\n".join(entries))

    def _render_cell(self, cell: Cell) -> List[str]:
        lines: int = 2 if cell.neighbor_s else 3
        cell_strs: List[str] = [""] * lines

        # Render the top line of the cell
        # Render the top left corner of the cell
        cell_strs[0] = f"{self.color_palette['wall']}█\033[0m"

        # Render the top wall of the cell
        if cell.north:
            cell_strs[0] += f"{self.color_palette['wall']}██\033[0m"
        elif cell.path == "N" or (cell.neighbor_n and cell.neighbor_n.path == "S"):
            cell_strs[0] += f"{self.color_palette['path']}╬╬\033[0m"
        else:
            cell_strs[0] += f"{self.color_palette['bg']}██\033[0m"

        # Render the top right corner of the cell
        cell_strs[0] += f"{self.color_palette['wall']}█\033[0m"

        # Render the center line of the cell
        # Render the left wall of the cell
        if cell.west:
            cell_strs[1] = f"{self.color_palette['wall']}█\033[0m"
        elif cell.path == "W" or (cell.neighbor_w and cell.neighbor_w.path == "E"):
            cell_strs[1] = f"{self.color_palette['path']}═\033[0m"
        else:
            cell_strs[1] = f"{self.color_palette['bg']}█\033[0m"

        # Render the center of the cell
        if cell.is_42:
            cell_strs[1] += f"{self.color_palette['42_pattern']}██\033[0m"
        elif cell.is_entry:
            cell_strs[1] += f"{self.color_palette['entry']}██\033[0m"
        elif cell.is_exit:
            cell_strs[1] += f"{self.color_palette['exit']}██\033[0m"
        elif cell.path:
            cell_strs[1] += f"{self.color_palette['path']}╬╬\033[0m"
        else:
            cell_strs[1] += f"{self.color_palette['bg']}██\033[0m"

        # Render the right wall of the cell
        if cell.east:
            cell_strs[1] += f"{self.color_palette['wall']}█\033[0m"
        elif cell.path == "E" or (cell.neighbor_e and cell.neighbor_e.path == "W"):
            cell_strs[1] += f"{self.color_palette['path']}═\033[0m"
        else:
            cell_strs[1] += f"{self.color_palette['bg']}█\033[0m"

        # Render the bottom line of the cell on last row (HARDCODED WALL)
        if lines == 3:
            cell_strs[2] = f"{self.color_palette['wall']}████\033[0m"
        return cell_strs

    def render_warnings(self, maze: Maze) -> None:
        if maze.warnings:
            for error in maze.warnings:
                stderr.write("\033[38;5;1m \033[48;5;1m WARNING: " + str(error) + "\033[0m\n")
            print()

    def render_maze(self, maze: Maze) -> None:
        maze_strs: List[str] = []
        for y in range(maze.height):
            lines = 2 if maze.get_cell(0, y).neighbor_s else 3
            maze_strs.extend([""]*lines)
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                cell_strs = self._render_cell(cell)
                maze_strs[y*2] += cell_strs[0]
                maze_strs[y*2+1] += cell_strs[1]
                if y == maze.height - 1:
                    maze_strs[y*2+2] += cell_strs[2]
        maze_str = "\n".join(maze_strs)
        print(maze_str, end="\n"*2)

    def render(self, maze: Maze) -> None:
        self.reset_terminal()
        self.render_maze(maze)
        self.render_warnings(maze)
        self.render_menu()
