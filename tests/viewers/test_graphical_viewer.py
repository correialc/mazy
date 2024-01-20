"""Tests for the graphical viewer."""
from unittest.mock import Mock, patch

import pytest

from mazy.builders.binary_tree_builder import BinaryTreeBuilder
from mazy.models.maze import MazeState
from mazy.viewers.graphical_viewer import (
    MazeGraphicalProcessor,
    MazeGraphicalViewer,
    CELL_SIZE,
    EXTERNAL_SIZE,
)


def test_graphical_viewer_default_values() -> None:
    """Ensure default values are consistent."""
    viewer = MazeGraphicalViewer(BinaryTreeBuilder(rows=2, cols=2))
    assert viewer.name == "graphical"


@patch("mazy.viewers.graphical_viewer.MazeGraphicalRenderer")
def test_graphical_viewer_calls_graphical_renderer(
    renderer_mock: Mock,
) -> None:
    """Should call the graphical renderer to show the maze."""
    viewer = MazeGraphicalViewer(BinaryTreeBuilder(rows=2, cols=2))
    viewer.show_maze()
    renderer_mock.assert_called()


def test_graphical_processor_not_animated() -> None:
    """Should create the graphical processor with a maze already built."""
    builder = BinaryTreeBuilder(rows=2, cols=3)
    processor = MazeGraphicalProcessor(builder, animated=False)

    assert processor.maze.state == MazeState.READY


def test_graphical_processor_animated() -> None:
    """Must build the maze step-by-step along the maze graphical processing."""
    builder = BinaryTreeBuilder(rows=2, cols=3)
    maze_size = builder.maze.rows * builder.maze.cols
    processor = MazeGraphicalProcessor(builder, animated=True)

    assert processor.maze.state == MazeState.BUILDING

    for _ in range(maze_size + 1):
        processor.process_maze()

    assert processor.maze.state == MazeState.READY  # type: ignore[comparison-overlap]


@pytest.mark.parametrize(("rows", "cols", "expected_centers"), [(2, 2, 3), (2, 3, 5)])
def test_graphical_processor_process_maze(
    rows: int,
    cols: int,
    expected_centers: int,
) -> None:
    """Should return a list of cell coordinate points."""
    builder = BinaryTreeBuilder(rows=rows, cols=cols)
    processor = MazeGraphicalProcessor(builder, animated=True)
    (
        border_points,
        unvisited_center_points,
        current_center_points,
    ) = processor.process_maze()

    assert len(border_points) > 0
    assert (
        len(unvisited_center_points) == expected_centers
    )  # Only the first cell visited

    for _ in range(rows * cols):
        (
            border_points,
            unvisited_center_points,
            current_center_points,
        ) = processor.process_maze()
        assert len(current_center_points) == 1

    assert len(unvisited_center_points) == 0  # All cell visited


@pytest.mark.parametrize(
    ("rows", "cols", "expected_delta"),
    [
        (2, 2, 96),
        (2, 3, 96),  # Number of columns is irrelevant
        (3, 3, 128),  # Number of rows is relevant
    ],
)
def test_graphical_processor_delta_y(
    rows: int,
    cols: int,
    expected_delta: int,
) -> None:
    """Should transport origin y-axis to upper-corner."""
    builder = BinaryTreeBuilder(rows, cols)
    processor = MazeGraphicalProcessor(builder, animated=False)
    assert processor.delta_y == rows * CELL_SIZE + EXTERNAL_SIZE
