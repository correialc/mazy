"""Tests for the solver model."""
from mazy.models.cell import Cell
from mazy.models.solver import Distances


def test_solver_distance_root_cell_default() -> None:
    """Should initialize the distance matrix with a root cell with default value."""
    distances = Distances(Cell(0, 0))
    assert distances.cells[distances.root] == 0
