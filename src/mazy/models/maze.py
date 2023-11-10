from enum import Enum
from typing import Generator, Sequence

from mazy.models.cell import Cell, Direction, Role


class MazeState(Enum):
    BUILDING = "building"
    READY = "ready"


class Maze:
    def __init__(self, rows: int, cols: int):
        self.state = MazeState.BUILDING
        self.rows = rows
        self.cols = cols
        self.cells: Sequence[Sequence[Cell]] = [
            [Cell(row, col) for col in range(cols)] for row in range(rows)
        ]
        self.registry_neighbors()

    def __getitem__(self, index: tuple[int, int]) -> Cell:
        i, j = index
        return self.cells[i][j]

    def registry_neighbors(self) -> None:
        self[0, 0].role = Role.ENTRANCE
        self[self.rows - 1, self.cols - 1].role = Role.EXIT

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self[row, col]

                if not cell.col == 0:
                    cell.link_to(
                        self[row, col - 1], passage=False, direction=Direction.WEST
                    )

                if not cell.row == 0:
                    cell.link_to(
                        self[row - 1, col], passage=False, direction=Direction.NORTH
                    )

    def traverse_by_cell(self) -> Generator[Cell, None, None]:
        for row in range(self.rows):
            for col in range(self.cols):
                yield self[row, col]
