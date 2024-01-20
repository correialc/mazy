"""Binary Tree Maze builder."""
import random
from typing import Generator

from mazy.builders.base_builder import MazeBuilder
from mazy.models.cell import Direction
from mazy.models.maze import Maze, MazeState

NAVIGATION_DIRECTIONS = [Direction.EAST, Direction.SOUTH]


class BinaryTreeBuilder(MazeBuilder):
    """Binary Tree Maze builder."""

    @property
    def name(self) -> str:
        """Builder name."""
        return "binary-tree"

    def build_maze(self) -> Generator[Maze, None, Maze]:
        """Build a maze using Binary Tree algorithm."""
        previous_cell = self.maze.current_cell
        for cell in self.maze.traverse_by_cell():
            choices = [
                direction
                for direction, neighbor in cell.neighbors.items()
                if not neighbor.passage and direction in NAVIGATION_DIRECTIONS
            ]

            if choices:
                target_direction: Direction = random.choice(choices)
                cell.carve_passage_to_direction(target_direction)

            self.update_cell_state(current_cell=cell, previous_cell=previous_cell)
            previous_cell = cell
            yield self.maze

        self.maze.state = MazeState.READY
        return self.maze
