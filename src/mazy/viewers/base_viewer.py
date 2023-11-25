"""Contracts for maze viewers."""
from abc import abstractmethod
from typing import Protocol

from mazy.builders.base_builder import MazeBuilder


class MazeViewer(Protocol):
    """Contract for maze viewers."""

    maze_builder: MazeBuilder

    @abstractmethod
    def show_maze(self) -> None:
        """Show the maze."""
        ...
