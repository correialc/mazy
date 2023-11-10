import random
from typing import Protocol, Generator

from mazy.models.maze import Maze


class MazeBuilder(Protocol):
    def build_maze(self, rows: int, cols: int) -> Generator[Maze, None, None]:
        ...