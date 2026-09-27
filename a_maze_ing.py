"""Módulo principal del proyecto A-ma-zing."""
import sys

from mazegen.config import Config, ConfigParser
from mazegen.maze import Maze
from mazegen.maze_generator import MazeGenerator, PerfectMazeGen, PacManMazeGen
from mazegen.renerer import Renderer

HEX_MAZE_25x20 = (
    "9139551111555515515395153",
    "ac2a9102829113855692c3a92",
    "814402aac42ac2a9138452a86",
    "a8116aa8552812c0028138683",
    "868696845142a8386846c6942",
    "81294143943a8284529553812",
    "8446943a852c2c4512a95286a",
    "a951292c2f816fffaac296852",
    "8416c2852fc4157f829285452",
    "81453ac56fffafff86aa8153a",
    "84112813913fafd503c2ac102",
    "812a82ac6c2fafffac54692aa",
    "aaaaa8453943c111413956aaa",
    "8682c453c43c3c6c3a82916c2",
    "83ac111451692915286a86956",
    "82c386815416c4292a9685693",
    "829429681141138444294552a",
    "ac69443aa83aa841392c39382",
    "839453a82c46845682812aa82",
    "c44556c6c555455546c446c46",
)


def menu_loop(conf: Config) -> None:
    generator: MazeGenerator = PacManMazeGen
    renderer: Renderer = Renderer()
    is_animated: Renderer | bool = False
    maze = generator.generate(conf, renderer=is_animated)
    while True:
        renderer.render(maze)
        choice = input("Enter your choice: ")
        if choice == "0":
            break
        elif choice == "1":
            conf.seed += 1
            maze: Maze = generator.generate(conf, renderer=is_animated)
        elif choice == "2":
            MazeGenerator.solve_maze(maze, renderer=is_animated)
        elif choice == "3":
            renderer.conmutate_color_palette()
        elif choice == "4":
            is_animated = renderer if not is_animated else False
        elif choice == "8":
            maze.save(conf.output_file)
        elif choice == "9":
            maze = Maze.load(conf.output_file)
        elif choice == "11":
            maze = Maze(hex_grid=HEX_MAZE_25x20, entry=(1, 1), exit=(19, 14))
            maze.set_path("ESEENEEESSSEESESSESESSSSEEEEEESES")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    path: str = sys.argv[1] if len(sys.argv) > 1 else "A-Maze-ing/config.txt"
    conf: Config = ConfigParser.load_config(path)
    menu_loop(conf)
