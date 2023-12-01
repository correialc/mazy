"""Binary Tree Maze builder."""
import random
from typing import Generator

from mazy.builders.base_builder import MazeBuilder
from mazy.models.cell import Direction
from mazy.models.maze import Maze, MazeState

NAVIGATION_DIRECTIONS = [Direction.EAST, Direction.SOUTH]


class SidewinderBuilder(MazeBuilder):
    """Binary Tree Maze builder."""

    @property
    def name(self) -> str:
        """Builder name."""
        return "sidewinder"

    def build_maze(self) -> Generator[Maze, None, Maze]:
        """Build a maze using Sidewinder algorithm."""
        run = []
        for cell in self.maze.traverse_by_cell():
            choices = [
                direction
                for direction, neighbor in cell.neighbors.items()
                if not neighbor.passage and direction in NAVIGATION_DIRECTIONS
            ]

            if choices:
                target_direction: Direction = random.choice(choices)

                if target_direction == Direction.EAST:
                    cell.carve_passage_to_direction(target_direction)
                    run.append(cell)
                else:
                    cell_from_run = random.choice(run) if len(run) else cell
                    cell_from_run.carve_passage_to_direction(target_direction)
                    run = []

            cell.visited = True
            yield self.maze

        self.maze.state = MazeState.READY
        return self.maze
