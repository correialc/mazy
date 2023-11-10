from mazy.models.cell import Direction, Role
from mazy.models.maze import Maze
from mazy.viewers.base_viewer import MazeViewer


class MazeTextViewer(MazeViewer):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def show_maze(self) -> None:
        print(self.maze_to_str())

    def maze_to_str(self) -> str:
        """Create an ASCII representation for a given maze."""
        maze_str = ""
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                cell = self.maze[row, col]
                maze_str += (
                    "+    "
                    if cell.has_passage_to_direction(Direction.NORTH)
                    or cell.role == Role.ENTRANCE
                    else "+----"
                )
                if col == self.maze.cols - 1:
                    maze_str += "+"
            maze_str += "\n"

            for col in range(self.maze.cols):
                cell = self.maze[row, col]
                maze_str += (
                    "     "
                    if cell.has_passage_to_direction(Direction.WEST)
                    else "|    "
                )
                if col == self.maze.cols - 1:
                    maze_str += "|"

            maze_str += "\n"
            if row == self.maze.rows - 1:
                maze_str += "+----" * (self.maze.cols - 1)
                maze_str += "+    +"

        return maze_str
