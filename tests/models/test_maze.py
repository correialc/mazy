import pytest

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
