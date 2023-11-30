"""Dummy builder."""
from mazy.builders.dummy_builder import DummyBuilder
from mazy.models.maze import MazeState
from mazy.utils import consume_generator


def test_dummy_builder_default_values() -> None:
    """Ensure default values are consistent."""
    builder = DummyBuilder(rows=2, cols=2)

    assert builder.name == "dummy"


def test_dummy_builder_build_maze() -> None:
    """Ensure each cell has no passages."""
    builder = DummyBuilder(rows=3, cols=5)
    maze = consume_generator(builder.build_maze())

    for cell in maze.traverse_by_cell():
        assert cell.passage_count() == 0


def test_dummy_builder_build_maze_set_visited_flag() -> None:
    """Should set the visited flag for each visited cell."""
    builder = DummyBuilder(rows=3, cols=5)

    for cell in builder.maze.traverse_by_cell():
        assert cell.visited is False

    maze = consume_generator(builder.build_maze())

    for cell in maze.traverse_by_cell():
        assert cell.visited is True


def test_dummy_builder_build_maze_manages_maze_states() -> None:
    """Ensure the builder set the correct state for each maze building step."""
    maze_generator = DummyBuilder(rows=3, cols=5).build_maze()

    assert next(maze_generator).state == MazeState.BUILDING
    assert consume_generator(maze_generator).state == MazeState.READY
