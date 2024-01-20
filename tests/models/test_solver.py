"""Tests for the solver model."""
import pytest

from mazy.models.cell import Cell
from mazy.models.solver import Distances


def test_solver_distance_root_cell_default() -> None:
    """Should initialize the distance matrix with a root cell with default value."""
    distances = Distances(root=Cell(0, 0))
    assert distances.cells[distances.root] == 0


def test_solver_distances_get_item() -> None:
    """Ensure values from the distance matrix can be queried by [] accessor."""
    cell = Cell(0, 0)
    distances = Distances(root=cell)
    assert distances[cell] == 0


def test_solver_distances_get_item_raises_when_key_is_not_cell() -> None:
    """Should raise an error if the key is not a Cell object."""
    cell = Cell(0, 0)
    distances = Distances(root=cell)

    with pytest.raises(
        ValueError,
        match="Only a Cell object can be used as key for the distance matrix!",
    ):
        _ = distances["invalid key"]  # type: ignore[index]


def test_solver_distances_set_item() -> None:
    """Ensure values from the distance matrix can be updated by [] accessor."""
    distances = Distances(root=Cell(0, 0))
    new_cell = Cell(0, 1)
    distances[new_cell] = 1
    assert distances[new_cell] == 1


def test_solver_distances_set_item_raises_when_key_is_not_cell() -> None:
    """Should raise an error if the key is not a Cell object."""
    cell = Cell(0, 0)
    distances = Distances(root=cell)

    with pytest.raises(
        ValueError,
        match="Only a Cell object can be used as key for the distance matrix!",
    ):
        distances["invalid key"] = 1  # type: ignore[index]


def test_solver_distances_set_item_raises_when_value_is_not_int() -> None:
    """Should raise an error if the value is not an integer."""
    cell = Cell(0, 0)
    distances = Distances(root=cell)

    with pytest.raises(
        ValueError,
        match="Only an integer number can be used as value for the distance matrix!",
    ):
        distances[cell] = "invalid value"  # type: ignore[assignment]
