import pytest

from mazy.models.maze import Maze, MazeState, calculate_cell_index


def test_maze_init() -> None:
    """Must generate a maze with a proper size and state."""
    maze = Maze(rows=2, cols=3)
    assert maze.state == MazeState.BUILDING
    assert maze.width == 3
    assert maze.height == 2


def test_maze_calculate_cell_index() -> None:
    """Should calculate a valid index for the given cell row and col."""
    maze = Maze(rows=2, cols=3)
    assert calculate_cell_index(maze.width, cell_row=0, cell_col=0) == 0
    assert calculate_cell_index(maze.width, cell_row=0, cell_col=1) == 1
    assert calculate_cell_index(maze.width, cell_row=0, cell_col=2) == 2
    assert calculate_cell_index(maze.width, cell_row=1, cell_col=0) == 3
    assert calculate_cell_index(maze.width, cell_row=1, cell_col=1) == 4


@pytest.mark.parametrize("row", [0, 1])
@pytest.mark.parametrize("col", [0, 1, 2])
def test_maze_get_cell(
    row: int,
    col: int,
) -> None:
    """Must return a cell for a given row and col."""
    maze = Maze(rows=2, cols=3)
    cell = maze.get_cell(row, col)
    assert cell.row == row
    assert cell.col == col
