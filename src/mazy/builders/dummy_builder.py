"""Binary Tree Maze builder."""
from typing import Generator

from mazy.builders.base_builder import MazeBuilder
from mazy.models.cell import Direction
from mazy.models.maze import Maze, MazeState

NAVIGATION_DIRECTIONS = [Direction.EAST, Direction.SOUTH]


class DummyBuilder(MazeBuilder):
    """Dummy Maze builder."""

    @property
    def name(self) -> str:
        """Builder name."""
        return "dummy"

    def build_maze(self) -> Generator[Maze, None, Maze]:
        """Build a maze without passages."""
        previous_cell = self.maze.current_cell
        for cell in self.maze.traverse_by_cell():
            self.update_cell_state(current_cell=cell, previous_cell=previous_cell)
            previous_cell = cell
            yield self.maze

        self.maze.state = MazeState.READY
        return self.maze
