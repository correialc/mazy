"""Tests for the Dijkstra's Shortest Path solver."""
from mazy.builders.dummy_builder import DummyBuilder
from mazy.models.cell import Direction
from mazy.models.maze import Maze
from mazy.models.solver import SolverAlgorithm
from mazy.solvers.dijkstra_shortest_path import DijkstraShortestPathSolver
from mazy.utils import consume_generator


def test_dijkstra_shortest_path_default_values() -> None:
    """Ensure default values are consistent."""
    builder = DummyBuilder(3, 5)
    maze = consume_generator(builder.build_maze())
    solver = DijkstraShortestPathSolver(maze)

    assert solver.name == SolverAlgorithm.DIJKSTRA_SHORTEST_PATH.value


def test_dijkstra_shortest_path_calculate_distances() -> None:
    """Should calculate the distance from the root cell for all the other cells."""
    maze = Maze(2, 3)

    root = maze[0, 0]
    root.carve_passage_to_direction(Direction.SOUTH)

    south_west_corner_cell = maze[1, 0]
    south_west_corner_cell.carve_passage_to_direction(Direction.EAST)

    south_central_cell = maze[1, 1]
    south_central_cell.carve_passage_to_direction(Direction.EAST)

    south_east_corner_cell = maze[1, 2]
    south_east_corner_cell.carve_passage_to_direction(Direction.NORTH)

    north_east_corner_cell = maze[0, 2]
    north_east_corner_cell.carve_passage_to_direction(Direction.WEST)

    north_central_cell = maze[0, 1]

    solver = DijkstraShortestPathSolver(maze)
    distances = solver.calculate_distances()

    assert distances[root] == 0
    assert distances[south_west_corner_cell] == 1
    assert distances[south_central_cell] == 2
    assert distances[south_east_corner_cell] == 3
    assert distances[north_east_corner_cell] == 4
    assert distances[north_central_cell] == 5
