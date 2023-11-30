"""Contract for maze builders."""
from abc import ABC, abstractmethod
from typing import Generator

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
