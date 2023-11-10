from unittest.mock import Mock, patch

from mazy.models.maze import Maze
from mazy.viewers.graphical_viewer import (CELL_SIZE, EXTERNAL_SIZE,
                                           MazeGraphicalProcessor,
                                           MazeGraphicalViewer, Wall)


@patch("mazy.viewers.graphical_viewer.MazeGraphicalRenderer")
def test_graphical_viewer_calls_graphical_renderer(
    renderer_mock: Mock,
) -> None:
    """Should call the graphical renderer to show the maze."""
    viewer = MazeGraphicalViewer(maze=Maze(2, 2))
    viewer.show_maze()
    renderer_mock.assert_called()


def test_graphical_processor_process_entrance_and_exit() -> None:
    maze = Maze(2, 2)
    processor = MazeGraphicalProcessor(maze)
    walls = processor.process_walls(maze[0, 0])

    assert len(walls) == 3
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
    maze = Maze(2, 3)
    processor = MazeGraphicalProcessor(maze)

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
