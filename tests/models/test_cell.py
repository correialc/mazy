from typing import Sequence

import pytest
from pytest import fixture

from mazy.models.cell import Border, Cell, Role, Direction


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


@pytest.mark.parametrize("bidirectional", [True, False])
def test_cell_add_link_to(
    bidirectional: bool,
) -> None:
    """ "Should link the current cell to another cell."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(cell2, Direction.NORTH, bidirectional=bidirectional)

    assert cell1.neighbors[Direction.NORTH] == cell2

    if bidirectional:
        assert cell2.neighbors[Direction.SOUTH] == cell1
    else:
        assert len(cell2.neighbors) == 0


def test_cell_add_link_default_bidirectional() -> None:
    """Should link cells bidirectionally by default."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(cell2, Direction.NORTH)

    assert cell1.neighbors[Direction.NORTH] == cell2
    assert cell2.neighbors[Direction.SOUTH] == cell1


@pytest.mark.parametrize("bidirectional", [True, False])
def test_cell_remove_link(
    bidirectional: bool,
) -> None:
    """Should unlink the current cell from another cell."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=1)
    cell1.link_to(cell2, Direction.NORTH, bidirectional=True)
    cell1.unlink_from(cell2, Direction.NORTH, bidirectional=bidirectional)

    assert cell2 not in cell1.neighbors.values()

    if bidirectional:
        assert cell1 not in cell2.neighbors.values()
    else:
        assert cell2.neighbors[Direction.SOUTH] == cell1


def test_cell_remove_link_default_bidirectional() -> None:
    """Should unlink cells bidirectionally by default."""
    cell1 = Cell(row=0, col=0)
    cell2 = Cell(row=0, col=0)
    cell1.link_to(cell2, Direction.NORTH)
    cell1.unlink_from(cell2, Direction.NORTH)

    assert cell2 not in cell1.neighbors.values()
    assert cell1 not in cell2.neighbors.values()
