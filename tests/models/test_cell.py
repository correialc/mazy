from typing import Sequence, Optional

import pytest
from pytest import fixture

from mazy.exceptions import NeighborhoodError, DuplicatedNeighbor, MissingLink
from mazy.models.cell import Border, Cell, Role, Direction, is_neighborhood_valid


@fixture
def cell_borders() -> Sequence[Border]:
    return [
        Border.TOP,
        Border.BOTTOM,
        Border.LEFT,
        Border.RIGHT,
        Border.TOP | Border.LEFT,
        Border.TOP | Border.RIGHT,
        Border.BOTTOM | Border.LEFT,
        Border.BOTTOM | Border.RIGHT,
        Border.TOP | Border.BOTTOM,
        Border.LEFT | Border.RIGHT,
        Border.TOP | Border.BOTTOM | Border.LEFT,
        Border.TOP | Border.BOTTOM | Border.RIGHT,
        Border.TOP | Border.LEFT | Border.RIGHT,
        Border.BOTTOM | Border.LEFT | Border.RIGHT,
        Border.BOTTOM | Border.LEFT | Border.RIGHT | Border.LEFT,
    ]


def test_cell_border_corner(cell_borders: Sequence[Border]) -> None:
    """Corner cells should have exactly 2 consecutive borders."""
    for border in cell_borders:
        if not border.bit_count() == 2 or border in [
            Border.TOP | Border.BOTTOM,
            Border.LEFT | Border.RIGHT,
        ]:
            assert border.corner is False
        else:
            assert border.corner is True


def test_cell_border_dead_end(cell_borders: Sequence[Border]) -> None:
    """Dead end cells should have exactly 3 borders."""
    for border in cell_borders:
        if border.bit_count() == 3:
            assert border.dead_end is True
        else:
            assert border.dead_end is False


def test_cell_border_intersection(cell_borders: Sequence[Border]) -> None:
    """Intersections should not have more than 1 border."""
    for border in cell_borders:
        if border.bit_count() < 2:
            assert border.intersection is True
        else:
            assert border.intersection is False


def test_cell_default_values() -> None:
    """Default values should be properly initialized."""
    cell = Cell(row=0, col=1)
    assert cell.border == Border.EMPTY
    assert cell.role == Role.NONE


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
    """ "Should link the current cell to another cell."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(cell2, Direction.EAST, bidirectional=bidirectional)

    assert cell1.neighbors[Direction.EAST] == cell2

    if bidirectional:
        assert cell2.neighbors[Direction.WEST] == cell1
    else:
        assert len(cell2.neighbors) == 0


def test_cell_add_link_default_bidirectional() -> None:
    """Should link cells bidirectionally by default."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(cell2, Direction.EAST)

    assert cell1.neighbors[Direction.EAST] == cell2
    assert cell2.neighbors[Direction.WEST] == cell1


def test_cell_add_link_validates_neighborhood() -> None:
    """Should validate the neighborhood before linking 2 cells."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)

    with pytest.raises(
        NeighborhoodError,
        match=r"The Cell\(row: 0, col: 1\) is not a valid neighbor on the north direction.",
    ):
        cell1.link_to(cell2, Direction.NORTH)


def test_cell_add_link_doesnt_overwrite_neighbor() -> None:
    """Can not create a link if there is a neighbor on the given direction."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(cell2, Direction.EAST)

    cell3 = Cell(row=0, col=1)

    with pytest.raises(
        DuplicatedNeighbor,
        match=r"The is already a neighbor for Cell\(row: 0, col: 0\) on the east direction.",
    ):
        cell1.link_to(cell3, Direction.EAST)


@pytest.mark.parametrize("bidirectional", [True, False])
def test_cell_remove_link(
    bidirectional: bool,
) -> None:
    """Should unlink the current cell from another cell."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(cell2, Direction.EAST, bidirectional=True)
    cell1.unlink_from(cell2, Direction.EAST, bidirectional=bidirectional)

    assert cell2 not in cell1.neighbors.values()

    if bidirectional:
        assert cell1 not in cell2.neighbors.values()
    else:
        assert cell2.neighbors[Direction.WEST] == cell1


def test_cell_remove_link_default_bidirectional() -> None:
    """Should unlink cells bidirectionally by default."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(cell2, Direction.EAST)
    cell1.unlink_from(cell2, Direction.EAST)

    assert cell2 not in cell1.neighbors.values()
    assert cell1 not in cell2.neighbors.values()


def test_cell_remove_link_validates_neighborhood() -> None:
    """Should validate the neighborhood before unlinking 2 cells."""
    cell1 = Cell(row=1, col=0)
    cell2 = Cell(row=0, col=0)
    cell1.link_to(cell2, Direction.NORTH)

    with pytest.raises(
        NeighborhoodError,
        match=r"The Cell\(row: 0, col: 0\) is not a valid neighbor on the east direction.",
    ):
        cell1.unlink_from(cell2, Direction.EAST)


def test_cell_remove_link_raises_when_neighbor_doesnt_exist() -> None:
    """Can not unlink 2 cells if there isn't a link between them."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)

    with pytest.raises(
        MissingLink,
        match=r"There is no link between Cell\(row: 0, col: 0\) and Cell\(row: 0, col: 1\) \(east direction\).",
    ):
        cell1.unlink_from(cell2, Direction.EAST)


@pytest.mark.parametrize(
    ("cell", "other_cell", "direction", "expected_result"),
    [
        (Cell(row=0, col=0), Cell(row=0, col=1), Direction.EAST, True),
        (Cell(row=0, col=0), Cell(row=0, col=1), None, False),
    ],
)
def test_cell_is_linked(
    cell: Cell, other_cell: Cell, direction: Optional[Direction], expected_result: bool
) -> None:
    """Should inform if there is a link between 2 cells."""
    if direction:
        cell.link_to(other_cell, direction)

    assert cell.is_linked(other_cell) == expected_result
