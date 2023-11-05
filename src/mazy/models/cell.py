from dataclasses import dataclass, field
from enum import IntEnum, IntFlag, auto, Enum
from typing import cast, Optional

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
class Neighbor:
    cell: "Cell"
    passage: bool


@dataclass
class Cell:
    row: int
    col: int

    border: Border = Border.TOP | Border.LEFT | Border.BOTTOM | Border.RIGHT
    role: Role = Role.NONE
    neighbors: dict[Direction, Neighbor] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"Cell(row: {self.row}, col: {self.col})"

    def link_to(
        self,
        other_cell: "Cell",
        passage: bool,
        direction: Direction,
        bidirectional: bool = True,
    ) -> None:
        if not is_neighborhood_valid(
            cell=self, neighbor=other_cell, direction=direction
        ):
            raise NeighborhoodError(
                f"{other_cell} position doesn't match the {direction.value} direction."
            )

        if self.neighbors.get(direction):
            raise DuplicatedNeighbor(
                f"The is already a neighbor for {self} on the east direction."
            )

        self.neighbors[direction] = Neighbor(cell=other_cell, passage=passage)

        if bidirectional:
            other_cell.neighbors[direction.opposite()] = Neighbor(
                cell=self, passage=passage
            )

    def unlink_from(
        self, other_cell: "Cell", direction: Direction, bidirectional: bool = True
    ) -> None:
        if not is_neighborhood_valid(
            cell=self, neighbor=other_cell, direction=direction
        ):
            raise NeighborhoodError(
                f"{other_cell} position doesn't match the {direction.value} direction."
            )

        if not self.neighbors.get(direction):
            raise MissingLink(
                f"There is no link from {self} to the {direction.value} direction."
            )

        del self.neighbors[direction]

        if bidirectional and other_cell.neighbors[direction.opposite()].cell == self:
            del other_cell.neighbors[direction.opposite()]

    def is_linked_to(self, other_cell: "Cell") -> bool:
        """Inform if 2 cells are linked (one is neighbor of the other)."""
        return other_cell in [neighbor.cell for neighbor in self.neighbors.values()]

    def has_passage_to_cell(self, other_cell: "Cell") -> bool:
        """Inform if there is a passage between 2 cells."""
        if self.is_linked_to(other_cell):
            return [
                neighbor.passage
                for neighbor in self.neighbors.values()
                if neighbor.cell == other_cell
            ].pop()

        return False

    def has_link_to_direction(self, direction: Direction) -> bool:
        """Inform if there is a link from the current cell to a given direction."""
        return self.neighbors.get(direction) is not None

    def has_passage_to_direction(self, direction: Direction) -> bool:
        """Inform if there is a passage from the current cell to a given direction."""
        if self.has_link_to_direction(direction):
            return self.neighbors[direction].passage

        return False

    def carve_passage_to_direction(self, direction: Direction) -> None:
        """Set the passage flag on a given direction.

        This operation is bidirectional.
        """
        if not self.has_link_to_direction(direction):
            raise MissingLink(
                f"There is no link from {self} to the {direction.value} direction."
            )

        neighbor = self.neighbors[direction]
        neighbor.passage = True

        other_cell = neighbor.cell

        if other_cell.has_link_to_direction(direction.opposite()):
            other_cell.neighbors[direction.opposite()].passage = True


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
