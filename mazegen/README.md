# mazegen

`mazegen` is a reusable Python module that generates and solves mazes.
It contains the core maze-generation logic independently from the configuration parser, terminal renderer, exporter, and interactive application.
It is designed to be imported as a standalone package in other projects.

## Public API

The package exposes:

- `MazeGenerator`
- `Maze`
- `Cell`

## Installation

The package is distributed as:

```text
mazegen-1.0.0.tar.gz
```

From the directory containing the archive, install it with:

```bash
python -m pip install ./mazegen-1.0.0.tar.gz
```

Using a virtual environment is recommended:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ./mazegen-1.0.0.tar.gz
```

## Import

Once installed:

```python
from mazegen import MazeGenerator
```

## Constructor

```python
MazeGenerator(width, height, entry, exit, perfect, seed=42)
```

## Custom parameters

`MazeGenerator` accepts the following parameters:

| Parameter | Description |
| --- | --- |
| `width` | Number of maze columns |
| `height` | Number of maze rows |
| `entry` | Entry coordinate as `(x, y)` |
| `exit_` | Exit coordinate as `(x, y)` |
| `perfect` | `True` for a perfect maze, `False` for an imperfect maze |
| `seed` | Optional seed for reproducible generation |


## Basic usage

```python
from mazegen import MazeGenerator

# Create a generator with a fixed seed
generator = MazeGenerator(
    width=21,
    height=15,
    entry=(0, 0),
    exit=(20, 14),
    perfect=True,
    seed=42,
)

# The generate() method yields intermediate maze states.
# The final item in the sequence is the finished maze.
frames = list(generator.generate())
maze = frames[-1]

print(maze)
print(f"Entry: ({maze.entry.x}, {maze.entry.y})")
print(f"Exit: ({maze.exit.x}, {maze.exit.y})")

# Access the shortest path solution (represented as directions 'N', 'E', 'S', 'W')
print(f"Solution path: {maze.path}")
```

## Notes

- `generate()` is a generator, so it is usually consumed with `for` or `list(...)`.
- The returned object is a `Maze` instance with useful properties such as `entry`, `exit`, `path`, and methods like `get_cell()` and `save()`.
- To render the maze in an application, iterate through the generated frames and display each state.

## Authors

Developed by **ilopez-g** and **mreyes-m** as part of the 42 curriculum.