from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import Iterator

from mazy.models.cell import Cell


class MazeState(Enum):
    BUILDING = "building"
    READY = "ready"


class Maze:
    def __init__(self, rows: int, cols: int):
        self.state = MazeState.BUILDING
        self.cells = tuple(
            [Cell(row, col) for row in range(rows) for col in range(cols)]
        )

    def __iter__(self) -> Iterator[Cell]:
        return iter(self.cells)

    def __getitem__(self, index: int) -> Cell:
        return self.cells[index]

    @cached_property
    def width(self) -> int:
        return max(cell.col for cell in self) + 1

    @cached_property
    def height(self) -> int:
        return max(cell.row for cell in self) + 1

    def get_cell(self, row: int, col: int) -> Cell:
        index = calculate_cell_index(self.width, row, col)
        return self[index]


def calculate_cell_index(maze_width: int, cell_row: int, cell_col: int) -> int:
    """Calculate the cell index based on its row and col."""
    return maze_width * cell_row + cell_col
