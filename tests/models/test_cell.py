from typing import Sequence
from pytest import fixture

from mazy.models.cell import Border, Cell, Role


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
    cell = Cell(row=0, col=0)
    assert cell.border == Border.EMPTY
    assert cell.role == Role.NONE
