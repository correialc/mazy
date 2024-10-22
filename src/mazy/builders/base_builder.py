"""Contract for maze builders."""
from abc import ABC, abstractmethod
from typing import Generator

from mazy.models.cell import Cell
from mazy.models.maze import Maze


class MazeBuilder(ABC):
    """Abstraction for maze builders."""

    def __init__(self, rows: int, cols: int):
        self.maze = Maze(rows, cols)

    @property
    @abstractmethod
    def name(self) -> str:
        """Builder name."""
        ...

    @abstractmethod
    def build_maze(self) -> Generator[Maze, None, Maze]:
        """Build a maze.

        Returns a Maze generator. This is useful to get each state of the
        maze during the building process.
        """
        ...

    def update_cell_state(self, current_cell: Cell) -> None:
        """Update the state of the cell for the current maze build step."""
        self.maze.previous_active_cells = set()
        for cell in self.maze.active_cells:
            cell.active = False
            self.maze.previous_active_cells.add(cell)

        current_cell.visited = True
        current_cell.active = True
        self.maze.active_cells = {current_cell}
