"""Dijkstra's Shortest Path maze solver."""
from typing import Optional

from mazy.models.cell import Cell
from mazy.models.solver import Distances
from mazy.solvers.base_solver import MazeSolver


class DijkstraShortestPathSolver(MazeSolver):
    """Dijkstra's Shortest Path maze solver."""

    @property
    def name(self) -> str:
        """Solver name."""
        return "dijkstra-shortest-path"

    def calculate_distances(self) -> Distances:
        """Given a maze, calculate the distance from the root cell to all the others.

        The calculation is made only for neighbor cells with a carved passage.
        """
        root = self.maze[0, 0]
        distances = Distances(root)

        frontier: list[tuple[Optional[Cell], Cell]] = [(None, root)]

        while len(frontier) > 0:
            new_frontier: list[tuple[Optional[Cell], Cell]] = []

            for previous_cell, current_cell in frontier:
                for neighbor_cell in current_cell.passages():
                    if neighbor_cell is not previous_cell:
                        distances[neighbor_cell] = distances[current_cell] + 1
                        new_frontier.append((current_cell, neighbor_cell))

            frontier = new_frontier

        return distances
