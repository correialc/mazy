"""Contract for maze solvers."""
from abc import ABC, abstractmethod

from mazy.models.maze import Maze


class MazeSolver(ABC):
    """Abstraction for maze solvers."""

    def __init__(self, maze: Maze):
        self.maze = maze

    @property
    @abstractmethod
    def name(self) -> str:
        """Solver name."""
        ...
