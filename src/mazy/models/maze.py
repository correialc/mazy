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
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(row, col) for col in range(cols)] for row in range(rows)]

    def __getitem__(self, index: tuple) -> Cell:
        i, j = index
        return self.cells[i][j]
