from abc import abstractmethod
from typing import Protocol

from mazy.models.maze import Maze


class MazeViewer(Protocol):
    maze: Maze

    @abstractmethod
    def show_maze(self) -> None:
        ...
