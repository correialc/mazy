"""Binary Tree Maze builder."""
import random
from typing import Generator

from mazy.models.cell import Direction
from mazy.models.maze import Maze

NAVIGATION_DIRECTIONS = [Direction.EAST, Direction.SOUTH]


class BinaryTreeBuilder:
    """Binary Tree Maze builder."""

    @staticmethod
    def build_maze(rows: int, cols: int) -> Generator[Maze, None, None]:
        """Build a maze using Binary Tree algorithm."""
        maze = Maze(rows, cols)

        for cell in maze.traverse_by_cell():
            choices = [
                direction
                for direction, neighbor in cell.neighbors.items()
                if not neighbor.passage and direction in NAVIGATION_DIRECTIONS
            ]

            if choices:
                target_direction: Direction = random.choice(choices)
                cell.carve_passage_to_direction(target_direction)

            yield maze
