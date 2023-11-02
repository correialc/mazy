from dataclasses import dataclass, field
from enum import IntEnum, IntFlag, auto, Enum
from typing import cast

from mazy.exceptions import NeighborhoodError, DuplicatedNeighbor, MissingLink


class Role(IntEnum):
    NONE = 0
    ENTRANCE = auto()
    EXIT = auto()
    EXTERIOR = auto()
    WALL = auto()


class Border(IntFlag):
    EMPTY = 0
    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()

    @property
    def is_square(self) -> bool:
        return self == cast(Border, self.TOP | self.LEFT | self.BOTTOM | self.RIGHT)

    @property
    def is_corner(self) -> bool:
        return self in (
            cast(Border, self.TOP | self.LEFT),
            cast(Border, self.TOP | self.RIGHT),
            cast(Border, self.BOTTOM | self.LEFT),
            cast(Border, self.BOTTOM | self.RIGHT),
        )

    @property
    def is_dead_end(self) -> bool:
        return self.bit_count() == 3

    @property
    def is_intersection(self) -> bool:
        return self.bit_count() < 2


class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

    def opposite(self) -> "Direction":
        direction: Direction
        match self:
            case self.NORTH:
                direction = self.SOUTH
            case self.SOUTH:
                direction = self.NORTH
            case self.EAST:
                direction = self.WEST
            case self.WEST:
                direction = self.EAST

        return direction


@dataclass
class Cell:
    row: int
    col: int

    border: Border = Border.TOP | Border.LEFT | Border.BOTTOM | Border.RIGHT
    role: Role = Role.NONE
    neighbors: dict[Direction, "Cell"] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"Cell(row: {self.row}, col: {self.col})"

    def link_to(
        self, other_cell: "Cell", direction: Direction, bidirectional: bool = True
    ) -> None:
        if not is_neighborhood_valid(
            cell=self, neighbor=other_cell, direction=direction
        ):
            raise NeighborhoodError(
                f"The {other_cell} is not a valid neighbor on the {direction.value} direction."
            )

        if self.neighbors.get(direction):
            raise DuplicatedNeighbor(
                f"The is already a neighbor for {self} on the east direction."
            )

        self.neighbors[direction] = other_cell

        if bidirectional:
            other_cell.neighbors[direction.opposite()] = self

    def unlink_from(
        self, other_cell: "Cell", direction: Direction, bidirectional: bool = True
    ) -> None:
        if not is_neighborhood_valid(
            cell=self, neighbor=other_cell, direction=direction
        ):
            raise NeighborhoodError(
                f"The {other_cell} is not a valid neighbor on the {direction.value} direction."
            )

        if not self.neighbors.get(direction):
            raise MissingLink(
                f"There is no link between {self} and {other_cell} (east direction)."
            )

        if self.neighbors[direction] == other_cell:
            del self.neighbors[direction]

        if bidirectional and other_cell.neighbors[direction.opposite()] == self:
            del other_cell.neighbors[direction.opposite()]

    def is_linked(self, other_cell: "Cell") -> bool:
        """Inform if 2 cells are linked (one is neighbor of the other)."""
        return other_cell in self.neighbors.values()


def is_neighborhood_valid(cell: Cell, neighbor: Cell, direction: Direction) -> bool:
    """Validate the neighborhood between 2 cells in a given direction.

    To be a valid neighborhood the two cells must have a difference
    of exactly 1 position on the given direction.
    """
    match direction:
        case direction.NORTH:
            if neighbor.row == cell.row - 1 and neighbor.col == cell.col:
                return True
        case direction.SOUTH:
            if neighbor.row == cell.row + 1 and neighbor.col == cell.col:
                return True
        case direction.EAST:
            if neighbor.row == cell.row and neighbor.col == cell.col + 1:
                return True
        case direction.WEST:
            if neighbor.row == cell.row and neighbor.col == cell.col - 1:
                return True

    return False
