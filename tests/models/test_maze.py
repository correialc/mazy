import pytest

from mazy.models.cell import Role, Direction
from mazy.models.maze import Maze, MazeState


def test_maze_init() -> None:
    """Must generate a maze with a proper size and state."""
    maze = Maze(rows=2, cols=3)
    assert maze.state == MazeState.BUILDING
    assert maze.rows == 2
    assert maze.cols == 3


def test_maze_cell_get_accessor() -> None:
    """Ensure individual cells of the maze can be accessed by row and col."""
    maze = Maze(rows=2, cols=3)
    cell = maze[0, 1]
    assert cell.row == 0
    assert cell.col == 1


def test_maze_registry_neighbors() -> None:
    """Should generate a valid maze.

    Entrance cell must be in the origin [0,0]
    Frontier cells should not have neighbors beyond their limits
    """
    maze = Maze(rows=3, cols=3)

    origin_cell = maze[0, 0]

    assert origin_cell.role == Role.ENTRANCE
    assert len(origin_cell.neighbors) == 2
    assert Direction.NORTH not in origin_cell.neighbors
    assert Direction.WEST not in origin_cell.neighbors
    assert Direction.SOUTH in origin_cell.neighbors
    assert Direction.EAST in origin_cell.neighbors

    middle_cell = maze[1, 1]
    assert len(middle_cell.neighbors) == 4
    assert Direction.NORTH in middle_cell.neighbors
    assert Direction.WEST in middle_cell.neighbors
    assert Direction.SOUTH in middle_cell.neighbors
    assert Direction.EAST in middle_cell.neighbors

    corner_cell = maze[2, 2]
    assert len(origin_cell.neighbors) == 2
    assert Direction.NORTH in corner_cell.neighbors
    assert Direction.WEST in corner_cell.neighbors
    assert Direction.SOUTH not in corner_cell.neighbors
    assert Direction.EAST not in corner_cell.neighbors
