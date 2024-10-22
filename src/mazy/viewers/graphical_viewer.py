"""Graphical viewer."""
import logging
from collections import namedtuple
from typing import Generator, cast, Tuple

from arcade import (
    Window,
    color,
    set_background_color,
    SpriteList,
    SpriteSolidColor,
    Sprite,
)

from mazy.builders.base_builder import MazeBuilder
from mazy.models.cell import Cell, Direction, Role
from mazy.models.maze import Maze, MazeState
from mazy.utils import consume_generator
from mazy.viewers.base_viewer import MazeViewer

logger = logging.getLogger(__name__)

SCREEN_TITLE = "Mazy"
BACKGROUND_COLOR = color.BLACK
BORDER_COLOR = color.GRAY
UNVISITED_CELL_COLOR = color.GRAY
VISITED_CELL_COLOR = color.BROWN
ACTIVE_CELL_COLOR = color.YELLOW

CELL_SIZE = 32
CELL_FILL_SIZE = 24
EXTERNAL_SIZE = 32

Point = namedtuple("Point", ["x", "y"])
Center = namedtuple("Center", ["center_x", "center_y"])


class MazeGraphicalViewer(MazeViewer):
    """Graphical viewer."""

    def __init__(self, maze_builder: MazeBuilder, animated: bool = False) -> None:
        self.maze_builder = maze_builder
        self.animated = animated
        self.name = "graphical"

    def show_maze(self) -> None:
        """Render and show the graphical representation of the maze."""
        logger.info(f"Loading graphical processor. Animated = {self.animated}")
        processor = MazeGraphicalProcessor(
            maze_builder=self.maze_builder, animated=self.animated
        )
        logger.info("Loading graphical renderer...")
        gui = MazeGraphicalRenderer(
            rows=self.maze_builder.maze.rows,
            cols=self.maze_builder.maze.cols,
            processor=processor,
        )
        logger.info("Start rendering...")
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
        self.processing = True

    @property
    def delta_y(self) -> int:
        """Transport origin y-axis from lower-corner to upper-corner."""
        return self.rows * CELL_SIZE + EXTERNAL_SIZE

    def calculate_cell_points(self, cell: Cell) -> tuple[list[Point], Point]:
        """Calculate primitive coordinates of the maze shapes."""
        start_x = EXTERNAL_SIZE + cell.col * CELL_SIZE
        start_y = self.delta_y - cell.row * CELL_SIZE

        end_x = EXTERNAL_SIZE + cell.col * CELL_SIZE + CELL_SIZE
        end_y = self.delta_y - cell.row * CELL_SIZE - CELL_SIZE

        center_point = Point(start_x + CELL_SIZE // 2, start_y - CELL_SIZE // 2)
        border_points = []

        # First horizontal line (frontier on NORTH)
        if not cell.role == Role.ENTRANCE and cell.row == 0:
            border_points.append(Point(start_x, self.delta_y))
            border_points.append(Point(end_x, self.delta_y))

        # First vertical line (frontier on WEST)
        if cell.col == 0:
            border_points.append(Point(EXTERNAL_SIZE, start_y))
            border_points.append(Point(EXTERNAL_SIZE, end_y))

        # Internal lines (horizontal walls)
        if (
            not cell.has_passage_to_direction(Direction.SOUTH)
            and cell.row < self.rows - 1
        ):
            border_points.append(Point(start_x, end_y))
            border_points.append(Point(end_x, end_y))

        # Internal lines (vertical wall)
        if (
            not cell.has_passage_to_direction(Direction.EAST)
            and cell.col < self.cols - 1
        ):
            border_points.append(Point(end_x, start_y))
            border_points.append(Point(end_x, end_y))

        # Last horizontal line (frontier on SOUTH)
        if not cell.role == Role.EXIT and cell.row == self.rows - 1:
            border_points.append(Point(start_x, EXTERNAL_SIZE))
            border_points.append(Point(end_x, EXTERNAL_SIZE))

        # Last vertical line (frontier on EAST)
        if cell.col == self.cols - 1:
            border_points.append(Point(end_x, self.delta_y))
            border_points.append(Point(end_x, EXTERNAL_SIZE))

        return border_points, center_point

    def process_maze(self) -> None:
        """Run the next round of maze processing."""
        if self.animated:
            next(self.maze_generator, None)

        if self.maze.state == MazeState.READY:
            self.processing = False
            logger.info("Maze processing finished.")


class MazeSprites:
    """Graphical representation of the maze using sprites."""

    def __init__(self, processor: MazeGraphicalProcessor):
        self.processor = processor
        self.sprites = SpriteList()
        self._create_sprites()

    def _create_sprites(self) -> None:
        """Create a sprite for each cell in the maze."""
        logger.info("Calculating primitive coordinates and creating sprites...")
        for cell in self.processor.maze.traverse_by_cell():
            border_points, center_point = self.processor.calculate_cell_points(cell)
            sprite = SpriteSolidColor(
                CELL_FILL_SIZE, CELL_FILL_SIZE, UNVISITED_CELL_COLOR
            )
            sprite.center_x = center_point.x
            sprite.center_y = center_point.y
            self.sprites.append(sprite)
        logger.info("Sprites created.")

    def lookup(self, cell: Cell) -> Sprite:
        """Find the sprite in the list based on the cell coordinates."""
        return cast(
            Sprite, self.sprites[cell.row * self.processor.maze.cols + cell.col]
        )

    def set_color(self, cell: Cell, new_color: Tuple[int, int, int]) -> None:
        """Lookup the sprite and set the color."""
        self.lookup(cell).color = new_color


class MazeGraphicalRenderer(Window):
    """Arcade graphical renderer.

    Extends Arcade Window object, drawing a window with
    a canvas for the maze graphical representation.
    """

    def __init__(self, rows: int, cols: int, processor: MazeGraphicalProcessor):
        logger.info("Arcade Graphical Engine detected.")

        self.processor = processor

        width = cols * CELL_SIZE + 2 * EXTERNAL_SIZE
        height = rows * CELL_SIZE + 2 * EXTERNAL_SIZE
        title = SCREEN_TITLE

        super().__init__(width=width, height=height, title=title)
        set_background_color(BACKGROUND_COLOR)

        self.maze_sprites = MazeSprites(self.processor)
        self.building_steps = 0

    def on_update(self, delta_time: float) -> None:
        """Update objects before rendering."""
        if self.processor.processing:
            self.processor.process_maze()

            for cell in self.processor.maze.previous_active_cells:
                self.maze_sprites.set_color(cell, VISITED_CELL_COLOR)

            for cell in self.processor.maze.active_cells:
                self.maze_sprites.set_color(cell, ACTIVE_CELL_COLOR)

    def on_draw(self) -> None:
        """Render all objects for the active window."""
        self.clear()
        self.maze_sprites.sprites.draw()  # type: ignore[no-untyped-call]
