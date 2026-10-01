# A-Maze-ing

Generador y visualizador de laberintos en terminal para Python. El proyecto crea laberintos perfectos o jugables, permite resolverlos por camino mínimo, cambiar la paleta visual y guardar/cargar estados del tablero.

## Descripción

Este proyecto implementa una aplicación de consola para generar laberintos con dos variantes:

- Laberinto perfecto: sin bucles, con una única ruta entre entrada y salida.
- Laberinto jugable: con caminos adicionales y cierta complejidad para simular un tablero más dinámico, similar a un mapa tipo Pac-Man.

La solución incluye:

- generación procedural del laberinto,
- validación de configuración,
- renderizado ASCII con colores en terminal,
- resolución del laberinto mediante BFS,
- guardado/carga del estado del laberinto,
- analizador de salida para comprobar coherencia y calidad del mazede.

## Estructura del proyecto

```text
A-Maze-ing/
├── a_maze_ing.py          # Punto de entrada de la aplicación
├── maze_analyzer.py       # Analiza un laberinto guardado y valida su estructura
├── config.txt             # Configuración por defecto
├── maze.txt               # Ejemplo de salida del laberinto
├── Makefile               # Comandos de uso rápido
├── pyproject.toml         # Configuración del paquete
├── LICENSE.md             # Licencia
├── mazegen/
│   ├── __init__.py
│   ├── config.py          # Carga y validación del archivo de configuración
│   ├── maze.py            # Modelo del laberinto y celdas
│   ├── maze_generator.py  # Generadores perfectos y jugables
│   └── renerer.py         # Renderizado y menús de terminal
└── mazegen.egg-info/      # Metadata del paquete
```

## Requisitos

- Python 3.10+
- Pydantic
- Terminal compatible con secuencias ANSI (para colores y limpieza del terminal)

## Instalación

Desde la raíz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si no existe `requirements.txt` en el proyecto, también puedes instalar las dependencias necesarias directamente:

```bash
pip install pydantic
```

## Ejecución

```bash
python3 a_maze_ing.py
```

O usando la configuración por defecto:

```bash
python3 a_maze_ing.py config.txt
```

También se puede ejecutar con el comando del `Makefile`:

```bash
make run
```

## Configuración

El archivo `config.txt` usa esta estructura:

```ini
WIDTH=21
HEIGHT=15
ENTRY=0,1
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Parámetros

- `WIDTH`: ancho del laberinto.
- `HEIGHT`: alto del laberinto.
- `ENTRY`: coordenadas de entrada en formato `x,y`.
- `EXIT`: coordenadas de salida en formato `x,y`.
- `OUTPUT_FILE`: archivo donde se guardará la salida del laberinto.
- `PERFECT`: si vale `True`, se genera un laberinto perfecto; si vale `False`, se genera una versión jugable con más caminos.
- `SEED`: valor semilla para generación reproducible.

## Menú de la aplicación

La interfaz ofrece estas opciones:

- `1`: Generar un nuevo laberinto
- `2`: Mostrar el camino más corto
- `3`: Cambiar la paleta de colores
- `4`: Activar/desactivar animación
- `8`: Guardar el laberinto actual
- `9`: Cargar un laberinto guardado
- `0`: Salir
- `11`: Cargar un laberinto predefinido de ejemplo `25x20`

## Generación del laberinto

La lógica de generación se implementa en `mazegen/maze_generator.py`:

- `PerfectMazeGen`: usa backtracking recursivo para crear un laberinto perfecto.
- `PacManMazeGen`: genera un laberinto más abierto y reutilizable, con múltiples rutas y más complejidad.

La composición del grid se basa en una representación por celdas, con paredes codificadas por bits y vecinos enlazados entre sí.

## Resolución del laberinto

La resolución usa BFS (Breadth-First Search) para encontrar el camino más corto desde la entrada hasta la salida.

- La ruta se almacena en cada celda.
- El renderizador resalta el recorrido en el terminal.
- Al resolver, el maze se actualiza visualmente con la ruta calculada.

## Analizador de laberintos

El script `maze_analyzer.py` valida un archivo de salida generado por el programa.

Comprueba:

- coherencia de las paredes compartidas entre celdas,
- si el laberinto es perfecto o jugable,
- si el número de bucles y dead-ends cumple los requisitos esperados,
- que la configuración del archivo sea válida y que el formato sea correcto.

### Ejemplo de uso

```bash
python3 maze_analyzer.py maze.txt
```

## Guardado y carga

El laberinto puede guardarse en un archivo con el formato de la aplicación y luego reabrirse para continuar la sesión.

```bash
python3 a_maze_ing.py config.txt
# luego -> opción 8 para guardar
# luego -> opción 9 para cargar
```

## Nota sobre el proyecto

Este proyecto está pensado como una práctica de generación procedural de laberintos, con énfasis en:

- estructuras de datos en Python,
- representación de grafos implícitos,
- validación de entradas,
- renderizado interactivo en terminal,
- análisis de trazas y caminos del laberinto.

## Comandos útiles

```bash
make install
make run
debug: make debug
make clean
make lint
make lint-strict
```

## Autoría

Proyecto desarrollado como parte de la práctica de 42 y adaptado para su uso desde la consola con un enfoque visual y reutilizable.
