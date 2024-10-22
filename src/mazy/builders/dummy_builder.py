"""Binary Tree Maze builder."""
import logging
from typing import Generator


from mazy.builders.base_builder import MazeBuilder
from mazy.models.cell import Direction
from mazy.models.maze import Maze, MazeState

logger = logging.getLogger()

NAVIGATION_DIRECTIONS = [Direction.EAST, Direction.SOUTH]


class DummyBuilder(MazeBuilder):
    """Dummy Maze builder."""

    @property
    def name(self) -> str:
        """Builder name."""
        return "dummy"

    def build_maze(self) -> Generator[Maze, None, Maze]:
        """Build a maze without passages."""
        for cell in self.maze.traverse_by_cell():
            self.update_cell_state(cell)
            self.maze.building_steps += 1
            yield self.maze

        self.maze.state = MazeState.READY
        logger.info(f"Maze created in {self.maze.building_steps} steps.")
        return self.maze
