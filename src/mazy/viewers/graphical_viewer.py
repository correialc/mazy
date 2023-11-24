"""Graphical viewer."""
from dataclasses import dataclass
from typing import Generator

from arcade import Window, color, draw_line, set_background_color

from mazy.builders.base_builder import MazeBuilder
from mazy.models.cell import Cell, Direction, Role
from mazy.models.maze import Maze
from mazy.utils import consume_generator
from mazy.viewers.base_viewer import MazeViewer

SCREEN_TITLE = "Mazy"
BACKGROUND_COLOR = color.BLACK
BORDER_COLOR = color.GRAY

CELL_SIZE = 32
EXTERNAL_SIZE = 32
ANIMATION_DELAY_SEC = 1


@dataclass
class Wall:
    """Primitive coordinates of a wall.

    In fact, a wall is a line representing the border
    of a cell.
    """

    x1: int
    y1: int
    x2: int
    y2: int


class MazeGraphicalViewer(MazeViewer):
    """Graphical viewer."""

    def __init__(self, maze_builder: MazeBuilder, animated: bool = False) -> None:
        self.maze_builder = maze_builder
        self.animated = animated

    def show_maze(self) -> None:
        """Render and show the graphical representation of the maze."""
        processor = MazeGraphicalProcessor(
            maze_builder=self.maze_builder, animated=self.animated
        )
        gui = MazeGraphicalRenderer(
            rows=self.maze_builder.maze.rows,
            cols=self.maze_builder.maze.cols,
            processor=processor,
        )
        gui.run()  # type: ignore[no-untyped-call]


class MazeGraphicalProcessor:
    """Process graphical information of the maze."""

    def __init__(self, maze_builder: MazeBuilder, animated: bool = False):
        self.rows = maze_builder.maze.rows
        self.cols = maze_builder.maze.cols
        self.maze_generator: Generator[Maze, None, Maze] = maze_builder.build_maze()
        self.maze = (
            maze_builder.maze if animated else consume_generator(self.maze_generator)
        )
        self.animated = animated

    @property
    def delta_y(self) -> int:
        """Transform origin y-axis from lower-corner to upper-corner."""
        return self.rows * CELL_SIZE + EXTERNAL_SIZE - 1

    def process_walls(self, cell: Cell) -> list[Wall]:
        """Calculate primitive coordinates of the maze walls."""
        x1 = EXTERNAL_SIZE + cell.col * CELL_SIZE
        y1 = self.delta_y - cell.row * CELL_SIZE

        x2 = EXTERNAL_SIZE + cell.col * CELL_SIZE + CELL_SIZE
        y2 = self.delta_y - cell.row * CELL_SIZE - CELL_SIZE

        walls = []

        # First horizontal line (frontier on NORTH)
        if not cell.role == Role.ENTRANCE and cell.row == 0:
            walls.append(Wall(x1, self.delta_y, x2, self.delta_y))

        # First vertical line (frontier on WEST)
        if cell.col == 0:
            walls.append(Wall(EXTERNAL_SIZE, y1, EXTERNAL_SIZE, y2))

        # Internal lines (horizontal walls)
        if (
            not cell.has_passage_to_direction(Direction.SOUTH)
            and cell.row < self.rows - 1
        ):
            walls.append(Wall(x1, y2, x2, y2))

        # Internal lines (vertical wall)
        if (
            not cell.has_passage_to_direction(Direction.EAST)
            and cell.col < self.cols - 1
        ):
            walls.append(Wall(x2, y1, x2, y2))

        # Last horizontal line (frontier on SOUTH)
        if not cell.role == Role.EXIT and cell.row == self.rows - 1:
            walls.append(Wall(x1, EXTERNAL_SIZE, x2, EXTERNAL_SIZE))

        # Last vertical line (frontier on EAST)
        if cell.col == self.cols - 1:
            walls.append(Wall(x2, self.delta_y, x2, EXTERNAL_SIZE))

        return walls

    def process_maze(self) -> Generator[Wall, None, None]:
        """Traverse the latest maze version processing graphical info."""
        if self.animated:
            next(self.maze_generator, None)

        for cell in self.maze.traverse_by_cell():
            for wall in self.process_walls(cell):
                yield wall


class MazeGraphicalRenderer(Window):
    """Arcade graphical renderer.

    Extends Arcade Window object, drawing a window with
    a canvas for the maze graphical representation.
    """

    def __init__(self, rows: int, cols: int, processor: MazeGraphicalProcessor):
        self.processor = processor

        width = cols * CELL_SIZE + 2 * EXTERNAL_SIZE
        height = rows * CELL_SIZE + 2 * EXTERNAL_SIZE
        title = SCREEN_TITLE

        super().__init__(width=width, height=height, title=title)
        set_background_color(BACKGROUND_COLOR)

    def on_draw(self) -> None:
        """Render all objects for the active window."""
        self.clear()

        for wall in self.processor.process_maze():
            draw_line(wall.x1, wall.y1, wall.x2, wall.y2, color=BORDER_COLOR)
