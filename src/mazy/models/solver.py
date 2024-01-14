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
    cells: dict[Cell, int] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        self.cells[self.root] = 0

    def __getitem__(self, key: Cell) -> int:
        if not isinstance(key, Cell):
            raise ValueError(
                "Only a Cell object can be used as key for the distance matrix!"
            )

        return self.cells[key]

    def __setitem__(self, key: Cell, value: int) -> None:
        if not isinstance(key, Cell):
            raise ValueError(
                "Only a Cell object can be used as key for the distance matrix!"
            )

        if not isinstance(value, int):
            raise ValueError(
                "Only an integer number can be used as value for the distance matrix!"
            )

        self.cells[key] = value
