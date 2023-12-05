"""Tests for the text (ASCII) viewer."""
import pytest

from mazy.builders.binary_tree_builder import BinaryTreeBuilder
from mazy.viewers.ascii_viewer import MazeTextViewer

ROW_SIZE = 2
COL_SIZE = 5


def test_graphical_viewer_default_values() -> None:
    """Ensure default values are consistent."""
    viewer = MazeTextViewer(BinaryTreeBuilder(rows=2, cols=2))
    assert viewer.name == "text"


@pytest.mark.parametrize(("rows", "cols"), [(2, 2), (2, 3), (3, 2)])
def test_ascii_viewer_maze_to_str(
    rows: int,
    cols: int,
) -> None:
    """Ensure the ASCII representation of the maze is consistent with the maze size."""
    builder = BinaryTreeBuilder(rows, cols)
    viewer = MazeTextViewer(builder)
    maze_str = viewer.maze_to_str()
    str_rows = maze_str.split("\n")
    assert len(str_rows) == ROW_SIZE * rows + 1

    # First row
    assert str_rows[0].startswith("+    +")
    assert str_rows[0].endswith("+----+")

    # Row in the middle
    assert str_rows[1].startswith("|    ")
    assert str_rows[1].endswith("    |")

    # Last row
    assert str_rows[-1].startswith("+----+")
    assert str_rows[-1].endswith("    +")

    for row in str_rows:
        assert len(row) == COL_SIZE * cols + 1


@pytest.mark.parametrize(("rows", "cols"), [(2, 2), (2, 3), (3, 2)])
@pytest.mark.parametrize(
    ("cell_content", "printed_content"),
    [
        ("X", " X  "),
        ("XY", " XY "),
        ("XYZ", "XYZ "),
        ("XYZW", "XYZW"),
    ],
)
def test_ascii_viewer_maze_to_str_with_cell_content(
    rows: int,
    cols: int,
    cell_content: str,
    printed_content: str,
) -> None:
    """Ensure cell content is properly printed when exists."""
    builder = BinaryTreeBuilder(rows, cols)
    viewer = MazeTextViewer(builder)

    for cell in builder.maze.traverse_by_cell():
        cell.content = cell_content

    maze_str = viewer.maze_to_str()

    assert maze_str.count(printed_content) == rows * cols
