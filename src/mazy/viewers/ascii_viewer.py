from mazy.models.cell import Direction, Role
from mazy.models.maze import Maze


def maze_to_str(maze: Maze) -> str:
    """Create an ASCII representation for a given maze."""
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
                "     " if cell.has_passage_to_direction(Direction.WEST) else "|    "
            )
            if col == maze.cols - 1:
                maze_str += "|"

        maze_str += "\n"
        if row == maze.rows - 1:
            maze_str += "+----" * (maze.cols - 1)
            maze_str += "+    +"

    return maze_str
