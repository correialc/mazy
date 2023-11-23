"""Tests for the binary tree builder."""
from mazy.builders.binary_tree_builder import BinaryTreeBuilder
from mazy.utils import consume_generator


def test_binary_tree_builder_build_maze() -> None:
    """Ensure each cell has at least 1 and no more than 3 passages."""
    maze = consume_generator(BinaryTreeBuilder.build_maze(3, 5))

    for cell in maze.traverse_by_cell():
        assert 0 < cell.passage_count() <= 3
