"""Módulo principal del proyecto A-ma-zing."""
import sys
from time import sleep

from app import Config, ConfigParser
from app import Renderer
from mazegen import Maze
from mazegen import MazeGenerator


def handle_generation(
        generator: MazeGenerator,
        renderer: Renderer,
        is_animated: bool
        ) -> Maze:
    """Generate a maze, optionally animating each generation step.

    Args:
        generator: Generator that yields the maze after each step.
        renderer: Renderer used to draw the animation frames.
        is_animated: Whether each intermediate step is drawn.

    Returns:
        The final generated maze.
    """
    maze: Maze = list(generator.generate())[-1]
    if is_animated:
        for maze in generator.generate():
            renderer.reset_terminal()
            renderer.render_maze(maze)
            sleep(1/30)
    return maze


def party_animation(renderer: Renderer, maze: Maze) -> None:
    """Generate an animation optionally, at number 5 option"""
    update = 0.005
    for i in range(100):
        renderer.conmutate_color_palette()
        renderer.reset_terminal()
        renderer.render_maze(maze)
        if i > 70:
            update += 0.01
            sleep(update)
        else:
            sleep(0.05)


def menu_loop(conf: Config) -> None:
    renderer: Renderer = Renderer()
    generator: MazeGenerator = MazeGenerator(
        conf.width,
        conf.height,
        conf.entry,
        conf.exit,
        conf.perfect,
        conf.seed
    )
    is_animated: bool = False
    maze: Maze = handle_generation(generator, renderer, is_animated)
    while True:
        renderer.render(maze)
        choice = input()
        if choice == "0":
            break
        elif choice == "1":
            maze = handle_generation(generator, renderer, is_animated)
        elif choice == "2":
            renderer.show_path = not renderer.show_path
        elif choice == "3":
            renderer.conmutate_color_palette()
        elif choice == "4":
            is_animated = not is_animated
        elif choice == "5":
            party_animation(renderer, maze)
        elif choice == "8":
            maze = Maze.load(conf.output_file)
        elif choice == "9":
            maze.save(conf.output_file)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage error: \"python3 a_maze_ing.py config.txt\"\n")
    try:
        path: str = sys.argv[1]
        conf: Config = ConfigParser.load_config(path)
        if conf:
            menu_loop(conf)
    except (KeyboardInterrupt, EOFError):
        sys.exit("Don't treat my program so badly, pay attention!")
