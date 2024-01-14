"""Models related to a cell."""
from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto
from typing import Optional
from uuid import UUID, uuid4

from mazy.exceptions import DuplicatedNeighbor, MissingLink, NeighborhoodError


class Role(IntEnum):
    """Possible roles for a cell."""

    NONE = 0
    ENTRANCE = auto()
    EXIT = auto()


class Direction(Enum):
    """Directions relative to the current cell."""

    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

    def opposite(self) -> "Direction":
        """The opposite direction relative to the current one."""
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
    """Cell linked to another cell in one direction.

    When a cell is next to the other in one direction, it is
    stored as a neighbor. A neigh can have or not a passage.
    """

    cell: "Cell"
    passage: bool


@dataclass
class Cell:
    """Basic building block of a maze."""

    row: int
    col: int

    role: Role = Role.NONE
    visited: bool = False
    solution: bool = False
    content: Optional[str] = None
    neighbors: dict[Direction, Neighbor] = field(default_factory=dict)

    _id: UUID = field(init=False, default_factory=uuid4)

    @property
    def id(self) -> UUID:
        """Immutable-like identification for a cell."""
        return self._id

    def __hash__(self) -> int:
        """Make the cell object hashable.

        Cells are mutable objects, but they need an immutable independent field
        to make possible to use cells in hashmaps even if the values of the cell
        attributes change along the time.
        """
        return hash(self._id)

    def __repr__(self) -> str:
        """Text representation of a Cell object."""
        return f"Cell(row: {self.row}, col: {self.col})"

    def link_to(
        self,
        other_cell: "Cell",
        passage: bool,
        direction: Direction,
        bidirectional: bool = True,
    ) -> None:
        """Link one cell to another creating a neighbor."""
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
        """Unlink one cell from the other removing a neighbor."""
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

    def passage_count(self) -> int:
        """Return current the number of passages for this cell."""
        return len(
            [
                neighbor.passage
                for neighbor in self.neighbors.values()
                if neighbor.passage
            ]
        )

    def passages(self) -> list["Cell"]:
        """Return the list of neighbor cells with a carved passage."""
        return [
            neighbor.cell for neighbor in self.neighbors.values() if neighbor.passage
        ]


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
