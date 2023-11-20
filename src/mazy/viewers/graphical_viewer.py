from dataclasses import dataclass
from typing import Generator

from arcade import Window, color, draw_line, set_background_color

from mazy.models.cell import Cell, Direction, Role
from mazy.models.maze import Maze
from mazy.viewers.base_viewer import MazeViewer

SCREEN_TITLE = "Mazy"
BACKGROUND_COLOR = color.BLACK
BORDER_COLOR = color.GRAY

CELL_SIZE = 32
EXTERNAL_SIZE = 32


@dataclass
class Wall:
    x1: int
    y1: int
    x2: int
    y2: int


class MazeGraphicalViewer(MazeViewer):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def show_maze(self) -> None:
        processor = MazeGraphicalProcessor(self.maze)
        gui = MazeGraphicalRenderer(
            rows=self.maze.rows, cols=self.maze.cols, processor=processor
        )
        gui.run()  # type: ignore[no-untyped-call]


class MazeGraphicalProcessor:
    def __init__(self, maze: Maze):
        self.maze = maze

    @property
    def delta_y(self) -> int:
        """Transform origin y-axis from lower-corner to upper-corner."""
        return self.maze.rows * CELL_SIZE + EXTERNAL_SIZE - 1

    def process_walls(self, cell: Cell) -> list[Wall]:
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
            and cell.row < self.maze.rows - 1
        ):
            walls.append(Wall(x1, y2, x2, y2))

        # Internal lines (vertical wall)
        if (
            not cell.has_passage_to_direction(Direction.EAST)
            and cell.col < self.maze.cols - 1
        ):
            walls.append(Wall(x2, y1, x2, y2))

        # Last horizontal line (frontier on SOUTH)
        if not cell.role == Role.EXIT and cell.row == self.maze.rows - 1:
            walls.append(Wall(x1, EXTERNAL_SIZE, x2, EXTERNAL_SIZE))

        # Last vertical line (frontier on EAST)
        if cell.col == self.maze.cols - 1:
            walls.append(Wall(x2, self.delta_y, x2, EXTERNAL_SIZE))

        return walls

    def process_maze(self) -> Generator[Wall, None, None]:
        for cell in self.maze.traverse_by_cell():
            for wall in self.process_walls(cell):
                yield wall


class MazeGraphicalRenderer(Window):
    def __init__(self, rows: int, cols: int, processor: MazeGraphicalProcessor):
        self.processor = processor

        width = cols * CELL_SIZE + 2 * EXTERNAL_SIZE
        height = rows * CELL_SIZE + 2 * EXTERNAL_SIZE
        title = SCREEN_TITLE

        super().__init__(width=width, height=height, title=title)
        set_background_color(BACKGROUND_COLOR)

    def on_draw(self) -> None:
        self.clear()

        for wall in self.processor.process_maze():
            draw_line(wall.x1, wall.y1, wall.x2, wall.y2, color=BORDER_COLOR)
