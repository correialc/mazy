"""Tests for the Dijkstra's Shortest Path solver."""
from mazy.builders.dummy_builder import DummyBuilder
from mazy.models.solver import SolverAlgorithm
from mazy.solvers.dijkstra_shortest_path import DijkstraShortestPathSolver
from mazy.utils import consume_generator


def test_dijkstra_shortest_path_default_values() -> None:
    """Ensure default values are consistent."""
    builder = DummyBuilder(3, 5)
    maze = consume_generator(builder.build_maze())
    solver = DijkstraShortestPathSolver(maze)

    assert solver.name == SolverAlgorithm.DIJKSTRA_SHORTEST_PATH.value
