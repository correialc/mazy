"""Tests for the graphical viewer."""
from unittest.mock import Mock, patch

from mazy.builders.binary_tree_builder import BinaryTreeBuilder
from mazy.models.maze import MazeState
from mazy.viewers.graphical_viewer import (
    MazeGraphicalProcessor,
    MazeGraphicalViewer,
)


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
