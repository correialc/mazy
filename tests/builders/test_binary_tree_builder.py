"""Tests for the binary tree builder."""
from mazy.builders.binary_tree_builder import BinaryTreeBuilder
from mazy.models.maze import MazeState
from mazy.utils import consume_generator


def test_binary_tree_builder_build_maze() -> None:
    """Ensure each cell has at least 1 and no more than 3 passages."""
    builder = BinaryTreeBuilder(rows=3, cols=5)
    maze = consume_generator(builder.build_maze())

    for cell in maze.traverse_by_cell():
        assert 0 < cell.passage_count() <= 3


def test_binary_tree_builder_build_maze_manages_maze_states() -> None:
    """Ensure the builder set the correct state for each maze building step."""
    maze_generator = BinaryTreeBuilder(rows=3, cols=5).build_maze()

    assert next(maze_generator).state == MazeState.BUILDING
    assert consume_generator(maze_generator).state == MazeState.READY
