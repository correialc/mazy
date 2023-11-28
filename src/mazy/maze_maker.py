"""CLI for maze generation."""
import logging
from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence

from mazy.builders.base_builder import MazeBuilder
from mazy.builders.binary_tree_builder import BinaryTreeBuilder
from mazy.viewers.ascii_viewer import MazeTextViewer
from mazy.viewers.base_viewer import MazeViewer
from mazy.viewers.graphical_viewer import MazeGraphicalViewer

logger = logging.getLogger(__name__)

DEFAULT_NUMBER_OF_ROWS = 3
DEFAULT_NUMBER_OF_COLS = 4
DEFAULT_MAZE_BUILDER = "binary-tree"
DEFAULT_MAZE_VIEWER = "graphical"


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
    parser.add_argument(
        "-v",
        "--viewer",
        type=str,
        default=DEFAULT_MAZE_VIEWER,
        help=f"Maze Viewer (default: {DEFAULT_MAZE_VIEWER}",
    )
    parser.add_argument(
        "-a", "--animated", action="store_true", help="Step-by-step animated building"
    )
    return parser.parse_args(args)


def make_maze(args: Namespace) -> None:
    """Make the maze and output results."""
    builder: MazeBuilder
    print(f"Loading {args.builder} builder...")
    match args.builder:
        case _:
            builder = BinaryTreeBuilder(args.rows, args.cols)
    print(f"{args.builder.capitalize()} builder loaded.")

    viewer: MazeViewer
    print(f"Loading {args.viewer} viewer...")
    match args.viewer:
        case "text":
            viewer = MazeTextViewer(builder)
        case _:
            viewer = MazeGraphicalViewer(builder, args.animated)
    print(f"{args.viewer.capitalize()} viewer loaded.")

    print(
        f"Building a {args.rows}x{args.cols} maze " f"using {args.builder} algorithm..."
    )

    print("Maze created.")
    viewer.show_maze()


if __name__ == "__main__":
    args = validate_args()
    make_maze(args)
