"""Tests for the cell model."""
from typing import Optional

import pytest

from mazy.exceptions import DuplicatedNeighbor, MissingLink, NeighborhoodError
from mazy.models.cell import Cell, Direction, Role, is_neighborhood_valid


def test_cell_default_values() -> None:
    """Default values should be properly initialized."""
    cell = Cell(row=0, col=1)
    assert cell.role == Role.NONE
    assert cell.visited is False
    assert cell.solution is False
    assert cell.content is None


def test_cell_is_hashable() -> None:
    """Ensure that objects of the Cell class are hashable."""
    cell = Cell(0, 0)
    assert hash(cell) == hash(cell.id)


def test_cell_identity_and_equality() -> None:
    """Should properly compare two instances of the Cell class."""
    cell = Cell(0, 0)
    same_cell = cell
    other_cell = Cell(0, 0)

    assert cell is same_cell
    assert cell == same_cell
    assert cell is not other_cell
    assert cell != other_cell


@pytest.mark.parametrize(
    ("direction", "expected_opposite"),
    [
        (Direction.NORTH, Direction.SOUTH),
        (Direction.SOUTH, Direction.NORTH),
        (Direction.EAST, Direction.WEST),
        (Direction.WEST, Direction.EAST),
    ],
)
def test_cell_opposite_direction(
    direction: Direction,
    expected_opposite: Direction,
) -> None:
    """Should return the opposite of a given direction."""
    assert direction.opposite() == expected_opposite


@pytest.mark.parametrize(
    ("cell", "neighbor", "direction", "expected_result"),
    [
        (Cell(row=0, col=0), Cell(row=0, col=1), Direction.EAST, True),
        (Cell(row=0, col=0), Cell(row=0, col=2), Direction.EAST, False),
        (Cell(row=0, col=0), Cell(row=1, col=0), Direction.EAST, False),
        (Cell(row=0, col=1), Cell(row=0, col=0), Direction.WEST, True),
        (Cell(row=0, col=2), Cell(row=0, col=0), Direction.WEST, False),
        (Cell(row=1, col=0), Cell(row=0, col=0), Direction.WEST, False),
        (Cell(row=1, col=0), Cell(row=0, col=0), Direction.NORTH, True),
        (Cell(row=2, col=0), Cell(row=0, col=0), Direction.NORTH, False),
        (Cell(row=0, col=1), Cell(row=0, col=0), Direction.NORTH, False),
        (Cell(row=0, col=0), Cell(row=1, col=0), Direction.SOUTH, True),
        (Cell(row=0, col=0), Cell(row=2, col=0), Direction.SOUTH, False),
        (Cell(row=0, col=0), Cell(row=0, col=1), Direction.NORTH, False),
    ],
)
def test_cell_validates_neighborhood(
    cell: Cell,
    neighbor: Cell,
    direction: Direction,
    expected_result: bool,
) -> None:
    """Must validate the consistence between the cells and the link direction."""
    assert is_neighborhood_valid(cell, neighbor, direction) == expected_result


@pytest.mark.parametrize("bidirectional", [True, False])
def test_cell_add_link_to(
    bidirectional: bool,
) -> None:
    """Should link the current cell to another cell."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(
        cell2, passage=False, direction=Direction.EAST, bidirectional=bidirectional
    )

    assert cell1.neighbors[Direction.EAST].cell == cell2

    if bidirectional:
        assert cell2.neighbors[Direction.WEST].cell == cell1
    else:
        assert len(cell2.neighbors) == 0


def test_cell_add_link_default_bidirectional() -> None:
    """Should link cells bidirectionally by default."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(cell2, passage=False, direction=Direction.EAST)

    assert cell1.neighbors[Direction.EAST].cell == cell2
    assert cell2.neighbors[Direction.WEST].cell == cell1


def test_cell_add_link_validates_neighborhood() -> None:
    """Should validate the cell row and col relative to the direction before linking."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)

    with pytest.raises(
        NeighborhoodError,
        match=r"Cell\(row: 0, col: 1\) position doesn't match the north direction.",
    ):
        cell1.link_to(cell2, passage=False, direction=Direction.NORTH)


def test_cell_add_link_doesnt_overwrite_neighbor() -> None:
    """Can not create a link if there is a neighbor on the given direction."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(cell2, passage=False, direction=Direction.EAST)

    cell3 = Cell(row=0, col=1)

    with pytest.raises(
        DuplicatedNeighbor,
        match=r"The is already a neighbor for Cell\(row: 0, col: 0\) "
        r"on the east direction.",
    ):
        cell1.link_to(cell3, passage=False, direction=Direction.EAST)


@pytest.mark.parametrize("bidirectional", [True, False])
def test_cell_remove_link(
    bidirectional: bool,
) -> None:
    """Should unlink the current cell from another cell."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(cell2, passage=False, direction=Direction.EAST, bidirectional=True)
    cell1.unlink_from(cell2, Direction.EAST, bidirectional=bidirectional)

    assert cell2 not in [neighbor.cell for neighbor in cell1.neighbors.values()]

    if bidirectional:
        assert cell1 not in [neighbor.cell for neighbor in cell2.neighbors.values()]
    else:
        assert cell2.neighbors[Direction.WEST].cell == cell1


def test_cell_remove_link_default_bidirectional() -> None:
    """Should unlink cells bidirectionally by default."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(cell2, passage=False, direction=Direction.EAST)
    cell1.unlink_from(cell2, Direction.EAST)

    assert cell2 not in [neighbor.cell for neighbor in cell1.neighbors.values()]
    assert cell1 not in [neighbor.cell for neighbor in cell2.neighbors.values()]


def test_cell_remove_link_validates_neighborhood() -> None:
    """Should validate cell row and col before unlinking from the direction."""
    cell1 = Cell(row=1, col=0)
    cell2 = Cell(row=0, col=0)
    cell1.link_to(cell2, passage=False, direction=Direction.NORTH)

    with pytest.raises(
        NeighborhoodError,
        match=r"Cell\(row: 0, col: 0\) position doesn't match the east direction.",
    ):
        cell1.unlink_from(cell2, Direction.EAST)


def test_cell_remove_link_raises_when_link_doesnt_exist() -> None:
    """Can not unlink 2 cells if there isn't a link on the given direction."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)

    with pytest.raises(
        MissingLink,
        match=r"There is no link from Cell\(row: 0, col: 0\) to the east direction.",
    ):
        cell1.unlink_from(cell2, Direction.EAST)


@pytest.mark.parametrize(
    ("cell", "other_cell", "direction", "expected_result"),
    [
        (Cell(row=0, col=0), Cell(row=0, col=1), Direction.EAST, True),
        (Cell(row=0, col=0), Cell(row=0, col=1), None, False),
    ],
)
def test_cell_is_linked_to(
    cell: Cell, other_cell: Cell, direction: Optional[Direction], expected_result: bool
) -> None:
    """Should inform if there is a link between 2 cells."""
    if direction:
        cell.link_to(other_cell, passage=False, direction=direction)

    assert cell.is_linked_to(other_cell) == expected_result


@pytest.mark.parametrize(
    ("cell", "other_cell", "direction", "passage", "expected_result"),
    [
        (Cell(row=0, col=0), Cell(row=0, col=1), Direction.EAST, True, True),
        (Cell(row=0, col=0), Cell(row=0, col=1), Direction.EAST, False, False),
        (Cell(row=0, col=0), Cell(row=0, col=1), None, False, False),
    ],
)
def test_cell_has_passage_to_cell(
    cell: Cell,
    other_cell: Cell,
    direction: Optional[Direction],
    passage: bool,
    expected_result: bool,
) -> None:
    """Should inform if there is a passage between 2 cells."""
    if direction:
        cell.link_to(other_cell, passage=passage, direction=direction)

    assert cell.has_passage_to_cell(other_cell) == expected_result


def test_cell_has_link_to_direction() -> None:
    """Should inform if there is a link from the cell to a given direction."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    _ = Cell(row=1, col=0)

    cell1.link_to(cell2, passage=False, direction=Direction.EAST)

    assert cell1.has_link_to_direction(Direction.EAST) is True
    assert cell1.has_link_to_direction(Direction.SOUTH) is False


@pytest.mark.parametrize(
    ("passage", "expected_result"),
    [(True, True), (False, False)],
)
def test_cell_has_passage_to_direction(
    passage: bool,
    expected_result: bool,
) -> None:
    """Should inform if there is a passage from the cell to a given direction."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    _ = Cell(row=1, col=0)

    cell1.link_to(cell2, passage=passage, direction=Direction.EAST)

    assert cell1.has_passage_to_direction(Direction.EAST) == passage
    assert cell1.has_passage_to_direction(Direction.SOUTH) is False


def test_cell_carve_passage_to_direction() -> None:
    """Should set passage flag to True in the given direction."""
    cell = Cell(row=0, col=0)
    other_cell = Cell(row=0, col=1)

    cell.link_to(other_cell, passage=False, direction=Direction.EAST)

    assert cell.has_passage_to_direction(Direction.EAST) is False
    assert other_cell.has_passage_to_direction(Direction.WEST) is False

    cell.carve_passage_to_direction(Direction.EAST)

    assert cell.has_passage_to_direction(Direction.EAST) is True
    assert other_cell.has_passage_to_direction(Direction.WEST) is True


def test_cell_carve_passage_to_direction_raises_when_link_doesnt_exist() -> None:
    """Can not carve a passage if there isn't a link on the given direction."""
    cell = Cell(row=0, col=0)

    with pytest.raises(
        MissingLink,
        match=r"There is no link from Cell\(row: 0, col: 0\) to the east direction.",
    ):
        cell.carve_passage_to_direction(Direction.EAST)


def test_cell_passage_count() -> None:
    """Should return the current number of passages."""
    cell = Cell(row=0, col=0)
    assert cell.passage_count() == 0

    cell_on_east = Cell(row=0, col=1)
    cell.link_to(cell_on_east, passage=True, direction=Direction.EAST)

    assert cell.passage_count() == 1

    cell_on_south = Cell(row=1, col=0)
    cell.link_to(cell_on_south, passage=True, direction=Direction.SOUTH)

    assert cell.passage_count() == 2


def test_cell_neighbors_with_carved_passage() -> None:
    """Should return the collection of neighbors cells with a carved passage."""
    cell = Cell(row=1, col=1)

    cell_on_east = Cell(row=1, col=2)
    cell.link_to(cell_on_east, passage=True, direction=Direction.EAST)
    cell_on_south = Cell(row=2, col=1)
    cell.link_to(cell_on_south, passage=True, direction=Direction.SOUTH)

    cell_on_west = Cell(row=1, col=0)  # Has no passage
    cell.link_to(cell_on_west, passage=False, direction=Direction.WEST)

    expected_cells = [cell_on_east, cell_on_south]

    assert cell.passages() == expected_cells
