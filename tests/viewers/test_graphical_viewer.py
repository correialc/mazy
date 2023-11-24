"""Tests for the graphical viewer."""
from unittest.mock import Mock, patch

from mazy.builders.binary_tree_builder import BinaryTreeBuilder
from mazy.models.maze import MazeState
from mazy.utils import consume_generator
from mazy.viewers.graphical_viewer import (
    CELL_SIZE,
    EXTERNAL_SIZE,
    MazeGraphicalProcessor,
    MazeGraphicalViewer,
    Wall,
)


@patch("mazy.viewers.graphical_viewer.MazeGraphicalRenderer")
def test_graphical_viewer_calls_graphical_renderer(
    renderer_mock: Mock,
) -> None:
    """Should call the graphical renderer to show the maze."""
    viewer = MazeGraphicalViewer(BinaryTreeBuilder(rows=2, cols=2))
    viewer.show_maze()
    renderer_mock.assert_called()


def test_graphical_processor_process_entrance_and_exit() -> None:
    """Should not draw a border neither for the ENTRANCE nor for the EXIT.

    The entrance can not have a border on the NORTH.
    The EXIT can not have a border on the SOUTH.
    """
    builder = BinaryTreeBuilder(rows=2, cols=2)
    maze = builder.maze
    processor = MazeGraphicalProcessor(builder)
    walls = processor.process_walls(maze[0, 0])

    assert len(walls) < 3
    assert (
        Wall(
            EXTERNAL_SIZE,
            processor.delta_y,
            EXTERNAL_SIZE + CELL_SIZE,
            processor.delta_y,
        )
        not in walls
    )

    walls = processor.process_walls(maze[1, 1])
    assert (
        Wall(
            EXTERNAL_SIZE + CELL_SIZE,
            EXTERNAL_SIZE,
            EXTERNAL_SIZE + 2 * CELL_SIZE,
            EXTERNAL_SIZE,
        )
        not in walls
    )


def test_graphical_processor_process_external_walls() -> None:
    """Must draw all the external walls except for the entrance and the exit."""
    builder = BinaryTreeBuilder(rows=2, cols=3)
    maze = builder.maze
    processor = MazeGraphicalProcessor(builder)

    cell = maze[0, 0]
    walls = processor.process_walls(cell)

    # NORTHWEST corner - Vertical
    assert (
        Wall(
            x1=EXTERNAL_SIZE,
            y1=processor.delta_y - cell.row * CELL_SIZE,
            x2=EXTERNAL_SIZE,
            y2=processor.delta_y - cell.row * CELL_SIZE - CELL_SIZE,
        )
        in walls
    )

    # SOUTHWEST corner - Vertical
    cell = maze[1, 0]
    walls = processor.process_walls(cell)
    assert (
        Wall(
            x1=EXTERNAL_SIZE,
            y1=processor.delta_y - cell.row * CELL_SIZE,
            x2=EXTERNAL_SIZE,
            y2=processor.delta_y - cell.row * CELL_SIZE - CELL_SIZE,
        )
        in walls
    )
    # SOUTHWEST corner - Horizontal
    assert (
        Wall(
            x1=EXTERNAL_SIZE + cell.col * CELL_SIZE,
            y1=EXTERNAL_SIZE,
            x2=EXTERNAL_SIZE + cell.col * CELL_SIZE + CELL_SIZE,
            y2=EXTERNAL_SIZE,
        )
        in walls
    )
    # NORTHEAST corner - Vertical
    cell = maze[0, 2]
    walls = processor.process_walls(cell)
    assert (
        Wall(
            x1=EXTERNAL_SIZE + cell.col * CELL_SIZE + CELL_SIZE,
            y1=processor.delta_y,
            x2=EXTERNAL_SIZE + cell.col * CELL_SIZE + CELL_SIZE,
            y2=EXTERNAL_SIZE,
        )
        in walls
    )
    # NORTHEAST corner - Vertical
    cell = maze[1, 2]
    walls = processor.process_walls(cell)
    assert (
        Wall(
            x1=EXTERNAL_SIZE + cell.col * CELL_SIZE + CELL_SIZE,
            y1=processor.delta_y,
            x2=EXTERNAL_SIZE + cell.col * CELL_SIZE + CELL_SIZE,
            y2=EXTERNAL_SIZE,
        )
        in walls
    )


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
        consume_generator(processor.process_maze())

    assert processor.maze.state == MazeState.READY  # type: ignore[comparison-overlap]
