from typing import Sequence, Optional

import pytest

from mazy.exceptions import NeighborhoodError, DuplicatedNeighbor, MissingLink
from mazy.models.cell import Border, Cell, Role, Direction, is_neighborhood_valid


@pytest.fixture
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


def test_cell_border_square(cell_borders: Sequence[Border]) -> None:
    """Square cells should have exactly 4 borders."""
    for border in cell_borders:
        if not border.bit_count() == 4:
            assert border.is_square is False
        else:
            assert border.is_square is True


def test_cell_border_corner(cell_borders: Sequence[Border]) -> None:
    """Corner cells should have exactly 2 consecutive borders."""
    for border in cell_borders:
        if not border.bit_count() == 2 or border in [
            Border.TOP | Border.BOTTOM,
            Border.LEFT | Border.RIGHT,
        ]:
            assert border.is_corner is False
        else:
            assert border.is_corner is True


def test_cell_border_dead_end(cell_borders: Sequence[Border]) -> None:
    """Dead end cells should have exactly 3 borders."""
    for border in cell_borders:
        if border.bit_count() == 3:
            assert border.is_dead_end is True
        else:
            assert border.is_dead_end is False


def test_cell_border_intersection(cell_borders: Sequence[Border]) -> None:
    """Intersections should not have more than 1 border."""
    for border in cell_borders:
        if border.bit_count() < 2:
            assert border.is_intersection is True
        else:
            assert border.is_intersection is False


def test_cell_default_values() -> None:
    """Default values should be properly initialized."""
    cell = Cell(row=0, col=1)
    assert cell.border.is_square
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
        match=r"The is already a neighbor for Cell\(row: 0, col: 0\) on the east direction.",
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
    """Should validate the cell row and col relative to the direction before unlinking."""
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
