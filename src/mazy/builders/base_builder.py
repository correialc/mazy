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

    def update_cell_state(self, current_cell: Cell, previous_cell: Cell) -> None:
        """Update the state of the cell for the current maze build step."""
        current_cell.visited = True

        if current_cell != previous_cell:
            previous_cell.current = False
            current_cell.current = True
            self.maze.current_cell = current_cell
