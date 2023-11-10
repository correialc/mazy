from unittest.mock import Mock, patch

import pytest
from _pytest.capture import CaptureFixture
from faker import Faker

from mazy.maze_maker import (DEFAULT_MAZE_BUILDER, DEFAULT_MAZE_VIEWER,
                             DEFAULT_NUMBER_OF_COLS, DEFAULT_NUMBER_OF_ROWS,
                             make_maze, validate_args)


@pytest.mark.parametrize(
    ("arg_short_name", "arg_name", "arg_value"),
    [
        pytest.param("-r", "--rows", 20, id="Number of rows"),
        pytest.param("-c", "--cols", 30, id="Number of columns"),
        pytest.param("-b", "--builder", "binary-tree", id="Binary Tree Builder"),
        pytest.param("-v", "--viewer", "graphical", id="Graphical Viewer"),
    ],
)
def test_maze_maker_validate_args(
    arg_short_name: str,
    arg_name: str,
    arg_value: str,
) -> None:
    """Should parse the provided args (short and long)."""
    args_namespace = validate_args([arg_name, str(arg_value)])
    assert getattr(args_namespace, arg_name.lstrip("-"), None) == arg_value

    args_namespace = validate_args([arg_short_name, str(arg_value)])
    assert getattr(args_namespace, arg_name.lstrip("-"), None) == arg_value


def test_maze_maker_validate_args_without_args() -> None:
    """Should the default values for all args."""
    args_namespace = validate_args([])
    assert getattr(args_namespace, "rows", None) == DEFAULT_NUMBER_OF_ROWS
    assert getattr(args_namespace, "cols", None) == DEFAULT_NUMBER_OF_COLS
    assert getattr(args_namespace, "builder", None) == DEFAULT_MAZE_BUILDER
    assert getattr(args_namespace, "viewer", None) == DEFAULT_MAZE_VIEWER


def test_maze_maker_validate_invalid_args(
    faker: Faker,
    capsys: CaptureFixture[str],
) -> None:
    """Should raise an error and provider a proper message for invalid args."""
    invalid_arg_name = f"--{faker.pystr()}"
    invalid_arg_value = faker.pystr()

    with pytest.raises(SystemExit):
        validate_args([invalid_arg_name, invalid_arg_value])

    captured = capsys.readouterr()
    assert (
        f"unrecognized arguments: {invalid_arg_name} {invalid_arg_value}"
        in captured.err
    )


@patch("mazy.maze_maker.MazeGraphicalViewer")
def test_maze_maker_make_maze_ascii_viewer(
    maze_graphical_viewer_mock: Mock,
    capsys: CaptureFixture[str],
) -> None:
    """Should validate args, make the maze and show in ASCII mode."""
    args_namespace = validate_args(["-r", "5", "-c", "8", "-v", "text"])
    make_maze(args_namespace)
    captured = capsys.readouterr()

    assert "Loading text viewer..."
    assert (
        f"Building a 5x8 maze using {DEFAULT_MAZE_BUILDER} algorithm..." in captured.out
    )
    assert "+    +----+" in captured.out
    assert "+----+    +" in captured.out
    assert "Maze created: 5x8" in captured.out
    maze_graphical_viewer_mock.assert_not_called()


@patch("mazy.maze_maker.MazeGraphicalViewer")
def test_maze_maker_make_maze_graphical_viewer(
    maze_graphical_viewer_mock: Mock,
    capsys: CaptureFixture[str],
) -> None:
    """Should validate args, make the maze and show in graphical mode."""
    args_namespace = validate_args(["-r", "5", "-c", "8", "-v", "graphical"])
    make_maze(args_namespace)
    captured = capsys.readouterr()

    assert "Loading graphical viewer..."
    assert (
        f"Building a 5x8 maze using {DEFAULT_MAZE_BUILDER} algorithm..." in captured.out
    )
    assert "Maze created: 5x8" in captured.out
    maze_graphical_viewer_mock.assert_called()
