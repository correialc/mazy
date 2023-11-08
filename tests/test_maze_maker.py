from argparse import ArgumentError
from typing import Optional

import pytest
from _pytest.capture import CaptureFixture
from faker import Faker

from mazy.maze_maker import (
    validate_args,
    make_maze,
    DEFAULT_NUMBER_OF_ROWS,
    DEFAULT_NUMBER_OF_COLS,
    DEFAULT_MAZE_BUILDER,
)


@pytest.mark.parametrize(
    ("arg_short_name", "arg_name", "arg_value"),
    [
        pytest.param("-r", "--rows", 20, id="Number of rows"),
        pytest.param("-c", "--cols", 30, id="Number of columns"),
        pytest.param("-b", "--builder", "binary-tree", id="Binary Tree Builder"),
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


@pytest.mark.parametrize("args", [[], ["-r", "5", "-c", "8"]])
def test_maze_maker_make_maze(
    args: list[str],
    capsys: CaptureFixture[str],
) -> None:
    """Should validate args, make the maze and provide a valid output."""
    args_namespace = validate_args(args)
    make_maze(args_namespace)
    captured = capsys.readouterr()

    expected_rows = args[1] if len(args) else DEFAULT_NUMBER_OF_ROWS
    expected_cols = args[3] if len(args) else DEFAULT_NUMBER_OF_COLS

    assert (
        f"Building a {expected_rows}x{expected_cols} maze using {DEFAULT_MAZE_BUILDER} algorithm..."
        in captured.out
    )
    assert "+    +----+" in captured.out
    assert "+----+    +" in captured.out
    assert f"Maze created: {expected_rows}x{expected_cols}" in captured.out
