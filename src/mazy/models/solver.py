"""Models related to maze solvers."""
from dataclasses import dataclass, field
from enum import Enum

from mazy.models.cell import Cell


class SolverAlgorithm(Enum):
    """Maze solver algorithms domain."""

    DIJKSTRA_SHORTEST_PATH = "dijkstra-shortest-path"


@dataclass
class Distances:
    """Distance matrix to support distance-based solvers."""

    root: Cell
    cells: dict[Cell, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.cells[self.root] = 0
