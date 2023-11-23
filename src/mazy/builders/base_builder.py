"""Contract for maze builders."""
from typing import Generator, Protocol

from mazy.models.maze import Maze


class MazeBuilder(Protocol):
    """Contract for maze builders."""

    def build_maze(self, rows: int, cols: int) -> Generator[Maze, None, None]:
        """Build a maze.

        Returns a Maze generator. This is useful to get each state of the
        maze during the building process.
        """
        ...
