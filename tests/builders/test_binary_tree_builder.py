from typing import Generator

from mazy.builders.binary_tree_builder import BinaryTreeBuilder
from mazy.models.maze import Maze


def test_binary_tree_builder_build_maze() -> None:
    """Ensure each cell has at least 1 and no more than 3 passages."""
    maze = _iter(BinaryTreeBuilder.build_maze(3, 5))

    for cell in maze.traverse_by_cell():
        assert 0 < cell.passage_count() <= 3


def _iter(maze_generator: Generator[Maze, None, None]) -> Maze:
    maze = next(maze_generator)
    while next_maze := next(maze_generator, None):
        maze = next_maze

    return maze
