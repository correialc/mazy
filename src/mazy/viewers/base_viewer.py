"""Contract for maze viewers."""
from abc import abstractmethod
from typing import Protocol

from mazy.models.maze import Maze


class MazeViewer(Protocol):
    """Contract for maze viewers."""

    maze: Maze

    @abstractmethod
    def show_maze(self) -> None:
        """Show the maze."""
        ...
