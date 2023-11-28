"""Text viewer."""
from mazy.builders.base_builder import MazeBuilder
from mazy.models.cell import Direction, Role
from mazy.utils import consume_generator
from mazy.viewers.base_viewer import MazeViewer


class MazeTextViewer(MazeViewer):
    """Text viewer."""

    def __init__(self, maze_builder: MazeBuilder) -> None:
        self.maze_builder = maze_builder
        self.name = "text"

    def show_maze(self) -> None:
        """Print a text representation of the maze."""
        print(self.maze_to_str())

    def maze_to_str(self) -> str:
        """Create an ASCII representation for a given maze."""
        maze = consume_generator(self.maze_builder.build_maze())
        maze_str = ""
        for row in range(maze.rows):
            for col in range(maze.cols):
                cell = maze[row, col]
                maze_str += (
                    "+    "
                    if cell.has_passage_to_direction(Direction.NORTH)
                    or cell.role == Role.ENTRANCE
                    else "+----"
                )
                if col == maze.cols - 1:
                    maze_str += "+"
            maze_str += "\n"

            for col in range(maze.cols):
                cell = maze[row, col]
                maze_str += (
                    "     "
                    if cell.has_passage_to_direction(Direction.WEST)
                    else "|    "
                )
                if col == maze.cols - 1:
                    maze_str += "|"

            maze_str += "\n"
            if row == maze.rows - 1:
                maze_str += "+----" * (maze.cols - 1)
                maze_str += "+    +"

        return maze_str
