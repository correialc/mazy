"""Binary Tree Maze builder."""
import logging
import random
from typing import Generator

from typing_extensions import override

from mazy.builders.base_builder import MazeBuilder
from mazy.models.cell import Direction, Cell
from mazy.models.maze import Maze, MazeState

logger = logging.getLogger()

NAVIGATION_DIRECTIONS = [Direction.EAST, Direction.SOUTH]


class SidewinderBuilder(MazeBuilder):
    """Binary Tree Maze builder."""

    @property
    def name(self) -> str:
        """Builder name."""
        return "sidewinder"

    @override
    def update_cell_state(self, current_cell: Cell) -> None:
        """Update the state of the cell for the current maze build step."""
        for cell in self.maze.active_cells:
            cell.active = False
            self.maze.previous_active_cells.add(cell)

    def build_maze(self) -> Generator[Maze, None, Maze]:
        """Build a maze using Sidewinder algorithm."""
        self.maze.active_cells = set()
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
                    cell.active = True
                    self.maze.active_cells.add(cell)
                else:
                    cell_from_run = (
                        random.choice(list(self.maze.active_cells))
                        if len(self.maze.active_cells)
                        else cell
                    )
                    cell_from_run.carve_passage_to_direction(target_direction)
                    self.update_cell_state(cell)

            cell.visited = True
            self.maze.building_steps += 1
            yield self.maze

        self.maze.state = MazeState.READY
        logger.info(f"Maze created in {self.maze.building_steps} steps.")
        return self.maze
