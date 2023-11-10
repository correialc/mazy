"""CLI for maze generation."""
import logging
from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence

from mazy.builders.binary_tree_builder import BinaryTreeBuilder
from mazy.utils import consume_generator
from mazy.viewers.ascii_viewer import maze_to_str

logger = logging.getLogger(__name__)

DEFAULT_NUMBER_OF_ROWS = 3
DEFAULT_NUMBER_OF_COLS = 4
DEFAULT_MAZE_BUILDER = "binary-tree"


def validate_args(args: Optional[Sequence[str]] = None) -> Namespace:
    """Parse the provided arguments and handle default values."""
    parser = ArgumentParser(description="Maze Generator")
    parser.add_argument(
        "-r",
        "--rows",
        type=int,
        default=DEFAULT_NUMBER_OF_ROWS,
        help=f"Number of rows (default: {DEFAULT_NUMBER_OF_ROWS})",
    )
    parser.add_argument(
        "-c",
        "--cols",
        type=int,
        default=DEFAULT_NUMBER_OF_COLS,
        help=f"Number of cols (default: {DEFAULT_NUMBER_OF_COLS})",
    )
    parser.add_argument(
        "-b",
        "--builder",
        type=str,
        default=DEFAULT_MAZE_BUILDER,
        help=f"Algorithm for maze building (default: {DEFAULT_MAZE_BUILDER}",
    )
    return parser.parse_args(args)


def make_maze(args_namespace: Namespace) -> None:
    """Make the maze and output results."""
    print(
        f"Building a {args_namespace.rows}x{args_namespace.cols} maze using {args_namespace.builder} algorithm..."
    )
    maze = consume_generator(
        BinaryTreeBuilder().build_maze(
            rows=args_namespace.rows, cols=args_namespace.cols
        )
    )
    print(maze_to_str(maze))
    print(f"Maze created: {maze.rows}x{maze.cols}")


if __name__ == "__main__":
    args_namespace = validate_args()
    make_maze(args_namespace)
