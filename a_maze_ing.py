"""Módulo principal del proyecto A-ma-zing."""
import sys
from time import sleep

from app.config import Config, ConfigParser
from app.renderer import Renderer
from mazegen.maze import Maze
from mazegen.maze_generator import MazeGenerator


def handle_generation(generator: MazeGenerator, renderer: Renderer, is_animated: bool) -> Maze:
    if is_animated:
        for maze in generator.generate():
            renderer.reset_terminal()
            renderer.render_maze(maze)
            sleep(1/30)
    else:
        maze: Maze = list(generator.generate())[-1]
    return maze


def menu_loop(conf: Config) -> None:
    renderer: Renderer = Renderer()
    generator = MazeGenerator(conf.width, conf.height, conf.entry, conf.exit, conf.perfect, conf.seed)
    is_animated = True
    maze: Maze = handle_generation(generator, renderer, is_animated)
    while True:
        renderer.render(maze)
        choice = input("Enter your choice: ")
        if choice == "0":
            break
        elif choice == "1":
            maze: Maze = handle_generation(generator, renderer, is_animated)
        elif choice == "2":
            list(generator.solve_maze(maze)) if not maze.path else maze.reset_path()
        elif choice == "3":
            renderer.conmutate_color_palette()
        elif choice == "4":
            is_animated = not is_animated
        elif choice == "8":
            maze.save(conf.output_file)
        elif choice == "9":
            maze = Maze.load(conf.output_file)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        path: str = sys.argv[1] if len(sys.argv) > 1 else "A-Maze-ing/config.txt"
        conf = None
        if path:
            conf: Config = ConfigParser.load_config(path)
        if conf:
            menu_loop(conf)
    except KeyboardInterrupt as e:
        print("No trates asi de mal a mi programa, imbecil!", e)
