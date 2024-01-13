"""Dijkstra's Shortest Path maze solver."""
from mazy.solvers.base_solver import MazeSolver


class DijkstraShortestPathSolver(MazeSolver):
    """Dijkstra's Shortest Path maze solver."""

    @property
    def name(self) -> str:
        """Solver name."""
        return "dijkstra-shortest-path"
