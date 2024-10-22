"""Tests for the command line CLI."""
import logging
from unittest.mock import Mock, patch

import pytest
from _pytest.capture import CaptureFixture
from _pytest.logging import LogCaptureFixture
from faker import Faker

from mazy.exceptions import InvalidBuilder, InvalidViewer
from mazy.maze_maker import (
    DEFAULT_MAZE_BUILDER,
    DEFAULT_MAZE_VIEWER,
    DEFAULT_NUMBER_OF_COLS,
    DEFAULT_NUMBER_OF_ROWS,
    make_maze,
    validate_args,
)
from mazy.models.builder import BuilderAlgorithm


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


@pytest.mark.parametrize(
    ("arg_short_name", "arg_name", "arg_value"),
    [
        pytest.param("-a", "--animated", True, id="Animated Building"),
    ],
)
def test_maze_maker_validate_flag_args(
    arg_short_name: str,
    arg_name: str,
    arg_value: str,
) -> None:
    """Should parse the provided flag args (short and long)."""
    args_namespace = validate_args([arg_name])
    assert getattr(args_namespace, arg_name.lstrip("-"), None) == arg_value

    args_namespace = validate_args([arg_short_name])
    assert getattr(args_namespace, arg_name.lstrip("-"), None) == arg_value


def test_maze_maker_validate_args_without_args() -> None:
    """Should the default values for all args."""
    args_namespace = validate_args([])
    assert getattr(args_namespace, "rows", None) == DEFAULT_NUMBER_OF_ROWS
    assert getattr(args_namespace, "cols", None) == DEFAULT_NUMBER_OF_COLS
    assert getattr(args_namespace, "builder", None) == DEFAULT_MAZE_BUILDER
    assert getattr(args_namespace, "viewer", None) == DEFAULT_MAZE_VIEWER
    assert getattr(args_namespace, "animated", None) is False


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


def test_maze_maker_raise_when_invalid_builder(
    faker: Faker,
) -> None:
    """Should raise an error when the builder is not valid."""
    invalid_builder_name = faker.pystr()
    args_namespace = validate_args(["-b", invalid_builder_name])
    with pytest.raises(
        InvalidBuilder, match=f"Invalid builder: {invalid_builder_name}"
    ):
        make_maze(args_namespace)


def test_maze_maker_raise_when_invalid_viewer(
    faker: Faker,
) -> None:
    """Should raise an error when the viewer is not valid."""
    invalid_viewer_name = faker.pystr()
    args_namespace = validate_args(["-v", invalid_viewer_name])
    with pytest.raises(InvalidViewer, match=f"Invalid viewer: {invalid_viewer_name}"):
        make_maze(args_namespace)


@pytest.mark.parametrize("builder_algorithm", [algo for algo in BuilderAlgorithm])
def test_maze_maker_build_maze(
    builder_algorithm: BuilderAlgorithm,
    capsys: CaptureFixture[str],
    caplog: LogCaptureFixture,
) -> None:
    """Should create a valid maze for every builder algorithm."""
    with caplog.at_level(logging.INFO):
        args_namespace = validate_args(["-b", builder_algorithm.value, "-v", "text"])
        make_maze(args_namespace)
        captured = capsys.readouterr()

        assert f"Loading {builder_algorithm.value} builder..." in caplog.text
        assert f"{builder_algorithm.value.capitalize()} builder loaded." in caplog.text
        assert "Loading text viewer..." in caplog.text
        assert "Text viewer loaded." in caplog.text
        assert (
            f"Building a 3x4 maze using {builder_algorithm.value} algorithm..."
            in caplog.text
        )

        assert "+    +----+" in captured.out
        assert "+----+    +" in captured.out


@patch("mazy.maze_maker.MazeGraphicalViewer")
def test_maze_maker_make_maze_ascii_viewer(
    maze_graphical_viewer_mock: Mock,
    capsys: CaptureFixture[str],
    caplog: LogCaptureFixture,
) -> None:
    """Should validate args, make the maze and show in ASCII mode."""
    with caplog.at_level(logging.INFO):
        args_namespace = validate_args(["-r", "5", "-c", "8", "-v", "text"])
        make_maze(args_namespace)
        captured = capsys.readouterr()

        assert f"Loading {DEFAULT_MAZE_BUILDER} builder..." in caplog.text
        assert f"{DEFAULT_MAZE_BUILDER.capitalize()} builder loaded." in caplog.text
        assert "Loading text viewer..." in caplog.text
        assert "Text viewer loaded." in caplog.text

        assert (
            f"Building a 5x8 maze using {DEFAULT_MAZE_BUILDER} algorithm..."
            in caplog.text
        )

        assert "+    +----+" in captured.out
        assert "+----+    +" in captured.out

        maze_graphical_viewer_mock.assert_not_called()


@patch("mazy.maze_maker.MazeGraphicalViewer")
def test_maze_maker_make_maze_graphical_viewer(
    maze_graphical_viewer_mock: Mock,
    caplog: LogCaptureFixture,
) -> None:
    """Should validate args, make the maze and show in graphical mode."""
    with caplog.at_level(logging.INFO):
        setattr(maze_graphical_viewer_mock, "identifier", "graphical")
        args_namespace = validate_args(["-r", "5", "-c", "8", "-v", "graphical"])
        make_maze(args_namespace)

        assert f"Loading {DEFAULT_MAZE_BUILDER} builder..." in caplog.text
        assert f"{DEFAULT_MAZE_BUILDER.capitalize()} builder loaded." in caplog.text
        assert "Loading graphical viewer..." in caplog.text
        assert "Graphical viewer loaded." in caplog.text

        assert (
            f"Building a 5x8 maze using {DEFAULT_MAZE_BUILDER} algorithm..."
            in caplog.text
        )

        maze_graphical_viewer_mock.assert_called()
