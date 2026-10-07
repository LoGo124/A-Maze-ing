*This project has been created as part of the 42 curriculum by i-lopez, mreyes-m.*

# A-Maze-ing 🧩

An algorithmic maze generator and solver built in Python. This project generates both **perfect mazes** and **braided mazes** (playable with zero dead-ends), allows for solving them via the shortest path from entry to exit, enables changes to the visual palette and supports saving and loading board states.

---

## 📋 Table of Contents
- [Description](#description)
- [Features](#-features)
- [Project Architecture](#-project-architecture)
- [Installation & Build](#-installation--build)
- [Run](#-cli-usage)
- [Configuration File Format](#-configuration-file-format)
- [`mazegen` Package Documentation](#-mazegen-package-documentation)
  - [Installation](#1-installation)
  - [Basic Usage Example](#2-basic-usage-example)
  - [Custom Parameters](#3-custom-parameters)
  - [Accessing Structure & Solution](#4-accessing-structure--solution)
- [Algorithms Implemented](#-algorithms-implemented)
- [Team & Project Management](#-license)
- [Bonus Features](#-license)
- [License](#-license)

---

## 📖 Description

**A-Maze-ing** is a maze generation and pathfinding visualization tool developed as part of the 42 curriculum. The project demonstrates:

- **Maze Generation**: Create random mazes using two different algorithms
- **Pathfinding**: Find the shortest path using BFS (Breadth-First Search)
- **Interactive Visualization**: Renders real-time ANSI terminal animations

---

## ✨ Features
* **Dual Generation Algorithms:**
  * **Recursive Backtracking (DFS):** Generates long, winding corridors.
  * **Randomized Prim's Algorithm:** Generates organic, highly-branched mazes.
* **42 Decorative Pattern:** Special 42 logo pattern 
* **BFS Pathfinding Solver:** Guarantees the shortest path from entry to exit.
* **Hexadecimal Wall Encoding:** Outputs grid wall states
* **Flicker-Free Terminal UI:** Showing generation and pathfinding.
* **Reusable Library (`mazegen`):** Packaged as a standalone `.whl` wheel for `pip`.

---

## 🏗️ Project Architecture

```text
.
├── a_maze_ing.py              # Main interactive application
├── config.txt                 # Default maze configuration
├── mazegen-1.0.0.tar.gz       # Installable reusable mazegen package
│
├── app/
│   ├── __init__.py
│   ├── config_parsing.py      # Pydantic-based configuration parser
│   └── renderer.py            # Terminal maze renderer
│
├── mazegen/
│   ├── __init__.py
│   ├── maze_generator.py      # Algorithms implementations
│   ├── maze.py                # Cell and Maze clases
│   └── README.md              # Documentation for the reusable package
│
├── .gitignore
├── LICENSE.md
├── Makefile
├── pyproject.toml             # Package/build configuration
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation & Build


### 1. Setting up the Virtual Environment
Is heavily recommended to use a Virtual Environment, so activate your own or create a new one: 

On bash with:
```bash
python3 -m venv .venv
```

Or using the `Makefile` rule:
```bash
make venv
```

Activate the Virtual Environment
```bash
source .venv/bin/activate
```

Then install the project dependencies:
```bash
make install
```

### 2. Building the `mazegen` Package
To compile the standalone wheel file from source:
```bash
pip install --upgrade build
python3 -m build
pip install mazegen-1.0.0.tar.gz
```

---

## 🚀 Run

The default configuration is stored in `config.txt`.
```bash
python3 a_maze_ing.py config.txt
```

Or using the `Makefile`:
```bash
make run
```

---

## 📄 Configuration File Format

The configuration file (`config.txt`) controls generator parameters:

```ini
WIDTH = 21
HEIGHT = 15
ENTRY = 0,0
EXIT = 20,14
OUTPUT_FILE = maze.txt
PERFECT = True
SEED = 42
```
### Options:
* `WIDTH`, `HEIGHT`: Grid dimensions (minimum 9, 7 required for '42' pattern).
* `ENTRY`, `EXIT`: Coordinates in `X,Y` format.
* `PERFECT`: `True` for single-path mazes; `False` for braided mazes ($0$ dead-ends).
* `SEED`: Integer seed for deterministic generation.

---

## 📦 `mazegen` Package Documentation

`mazegen` is the reusable maze-generation package developed for the **A-Maze-ing** project.

### 1. Installation
Install the pre-built wheel directly via `pip`:

```bash
pip install mazegen-1.0.0.tar.gz
```

### 2. Basic Usage Example
```python
from mazegen import MazeGenerator

# Build the generator with the maze dimensions and coordinates
generator = MazeGenerator(
    width=21,
    height=15,
    entry=(0, 0),
    exit=(20, 14),
    perfect=False,
    seed=42,
)

# Generate the maze. This yields successive states until the final solved maze.
frames = list(generator.generate())
final_maze = frames[-1]

print(final_maze)
print(f"Entry: ({final_maze.entry.x}, {final_maze.entry.y})")
print(f"Exit: ({final_maze.exit.x}, {final_maze.exit.y})")
print(f"Solution path: {final_maze.path}")
```

The `generate()` method is a generator, so it is typically consumed with `for` or `list(...)` to obtain the final maze state.

### 3. Custom Parameters

| Parameter | Description |
| :--- | :--- |
| `width` | Horizontal grid size |
| `height` | Vertical grid size |
| `entry` | Entrance coordinates `(x, y)` |
| `exit` | Exit coordinates `(x, y)` |
| `perfect` | `True` for a perfect maze, `False` for a braided maze |
| `seed` | Random seed for reproducible generation |

### 4. Accessing Structure & Solution

```python
# Access individual cells
cell = maze.get_cell(x=5, y=3)

# Check cell wall states 
print(f"Hex Wall Value: {cell.hex_val}") # e.g. 'f', 'b', '0'
print(f"North Wall Closed? {cell.north}")
print(f"Is 42 Pattern? {cell.is_42}")

# Access the solution (represented as 'N', 'E', 'S', 'W')
print(f"Solution Path: {maze.path}")
```

### 5. Rebuilding the package

All elements required to rebuild the reusable package are included in the repository.

```bash
make build
```
The standard Python build process creates the package distributions inside dist/. The source distribution submitted with the project is copied to the repository root as mazegen-1.0.0.tar.gz.

---

## 🧠 Algorithms Implemented

### 1. Recursive Backtracking (DFS) (`PERFECT = True`)
**How it works:**
1. Start at a random cell and mark it as visited
2. While there are unvisited cells:
   - If current cell has unvisited neighbors:
     - Choose a random unvisited neighbor
     - Remove the wall between current and chosen cell
     - Move to the chosen cell and mark it visited
     - Push current cell to stack
   - Else:
     - Pop a cell from the stack and backtrack

- **Generates perfect mazes**: Every maze has exactly one solution with no loops
- **Long, winding passages**: Creates aesthetically pleasing mazes with long corridors
- **Consistent quality**: Always produces solvable, challenging mazes

### 2. Prim's Algorithm (`PERFECT = False`)

**How it works:**
1. Start with a grid full of walls
2. Pick a random cell, mark it as part of the maze
3. Add the cell's neighbors to a "frontier" list
4. While the frontier is not empty:
   - Pick a random frontier cell
   - Connect it to a random adjacent cell already in the maze
   - Add its unvisited neighbors to the frontier

- **Different maze characteristics**: Creates mazes with more branching patterns
- **Randomized structure**: More unpredictable maze layouts

### 3. Breadth-First Search (BFS)

**How it works:**
1.  BFS starts at the entry node and explores the maze layer by layer, visiting all immediate, adjacent neighbors before advancing to deeper levels
2. It utilizes a First-In, First-Out (FIFO) queue to queue unexplored nodes and maintains a visited tracker to prevent processing the same cell twice or entering infinite loops

- **Guaranteed Shortest Path**: Because it expands uniformly outward in increasing order of distance from the source, the moment BFS reaches the exit cell, it mathematically guarantees finding the shortest valid path in unweighted graphs

---

## 📚 Resources & AI Declaration

### References Consulted
* *GeeksforGeeks*: Breadth First Search or BFS for a Graph
* *Buckblog*: Maze Generation: Prim's Algorithm (Jamis Buck)
* *Jonathan Zong*: Maze Generation with Prim's Algorithm
* *Build your own Command Line with ANSI escape codes*: Terminal rendering and cursor movement (`\033[H`)

### AI Usage Declaration
In accordance with 42 curriculum guidelines, AI assistance was utilized for:
* Explaining bitwise wall bitmask operations and clarifying maze-generation concepts
* Discussing possible project architecture and module separation
* Formatting `pyproject.toml` according to PEP 517 / PEP 621 standards.
* Assisting with organization of project documentation

---

## 👥 Team & Project Management

### Team Members & Roles
* **`ilopez-g`**: Core data structure architecture, `config.txt` parser, ANSI terminal renderer UI and `pyproject.toml` wheel packaging.
* **`mreyes-m`**: Generation algorithms (`Recursive Backtracker`, `Prim's Algorithm`), `Braiding` post-processor and `BFS` solver

### Planning vs. Actual Execution
* **Planning:** Designed `Cell` and `Maze` classes with bitwise wall masks and neighbor pointers.
* **Algorithmic Core:** Implemented Prim's and Backtracking generators along with the '42' pattern overlay.
* **Solver & UI:** Integrated BFS pathfinder and flicker-free terminal rendering with ANSI codes.
* **Refactoring & Packaging:** Separated application logic into `app/` and core generation library into `mazegen/`, compiling the final `.whl` wheel.

### Retrospective
* **What went well:** Fast, flicker-free terminal UI and robust 0-dead-end braiding.
* **Improvements for future:** Add interactive keyboard controls for real-time algorithm switching and delay adjustment during rendering.
* **Tools Used:** Git, VS Code, `flake8`, `mypy`, `python -m build`, Python standard library.

---

## ✨ Bonus Features
* **Multiple generation algorithms:** Recursive Backtracking and Prim
* **Animated maze generation:** Maze construction can be displayed step by step using generators and yield
* **Animated solution path:** Shortest path can be displayed progressively
* **Dead-end removal:** Imperfect mazes are processed to remove dead ends
* **Automatic entry/exit relocation:** If the configured entry or exit overlaps the 42 pattern, it is automatically moved to the nearest valid cell
* **Color gambling:** Animated terminal effect that continuously changes the maze colors

---

## 📜 License

This project is licensed under the **GNU GENERAL PUBLIC LICENSE** - see the [LICENSE.md](LICENSE.md) file for details.

