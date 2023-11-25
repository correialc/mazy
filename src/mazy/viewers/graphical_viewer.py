"""Graphical viewer."""
import timeit
from collections import namedtuple
from dataclasses import dataclass
from typing import Any, Generator, NamedTuple, Optional

from arcade import (
    Shape,
    ShapeElementList,
    Window,
    color,
    create_lines,
    create_rectangle,
    create_rectangles_filled_with_colors,
    draw_line,
    draw_text,
    set_background_color,
)

from mazy.builders.base_builder import MazeBuilder
from mazy.models.cell import Cell, Direction, Role
from mazy.models.maze import Maze
from mazy.utils import consume_generator
from mazy.viewers.base_viewer import MazeViewer

SCREEN_TITLE = "Mazy"
BACKGROUND_COLOR = color.BLACK
BORDER_COLOR = color.GRAY
UNVISITED_CELL_COLOR = color.BEIGE

CELL_SIZE = 32
EXTERNAL_SIZE = 32
ANIMATION_DELAY_SEC = 1

Point = namedtuple("Point", ["x", "y"])
Center = namedtuple("Center", ["center_x", "center_y"])


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

    def process_maze(self) -> tuple[list[Point], list[Point]]:
        """Traverse the latest maze version processing graphical info."""
        if self.animated:
            next(self.maze_generator, None)

        cell_border_points = []
        cell_center_points = []

        for cell in self.maze.traverse_by_cell():
            border_points, center_point = self.calculate_cell_points(cell)
            cell_border_points.extend(border_points)

            if not cell.visited:
                cell_center_points.append(center_point)

        return cell_border_points, cell_center_points


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

        self.maze_shapes: ShapeElementList[Shape | Any] = ShapeElementList()  # type: ignore[no-untyped-call]

    def on_update(self, delta_time: float) -> None:
        """Update objects before rendering."""
        border_points, center_points = self.processor.process_maze()
        self.maze_shapes = ShapeElementList()  # type: ignore[no-untyped-call]

        for center in center_points:
            self.maze_shapes.append(
                create_rectangle(
                    center_x=center.x,
                    center_y=center.y,
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                    color=UNVISITED_CELL_COLOR,
                )
            )

        self.maze_shapes.append(
            create_lines(point_list=border_points, color=BORDER_COLOR)
        )

    def on_draw(self) -> None:
        """Render all objects for the active window."""
        self.clear()
        self.maze_shapes.draw()  # type: ignore[no-untyped-call]
