from dataclasses import dataclass, field
from enum import IntEnum, IntFlag, auto, Enum


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
    def corner(self) -> bool:
        return self in (
            self.TOP | self.LEFT,
            self.TOP | self.RIGHT,
            self.BOTTOM | self.LEFT,
            self.BOTTOM | self.RIGHT,
        )

    @property
    def dead_end(self) -> bool:
        return self.bit_count() == 3

    @property
    def intersection(self) -> bool:
        return self.bit_count() < 2


class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

    def opposite(self) -> "Direction":
        match self:
            case self.NORTH:
                return self.SOUTH
            case self.SOUTH:
                return self.NORTH
            case self.EAST:
                return self.WEST
            case self.WEST:
                return self.EAST


@dataclass
class Cell:
    row: int
    col: int
    border: Border = Border.EMPTY
    role: Role = Role.NONE
    neighbors: dict[Direction, "Cell"] = field(default_factory=dict)

    def link_to(
        self, other_cell: "Cell", direction: Direction, bidirectional: bool = True
    ) -> None:
        self.neighbors[direction] = other_cell

        if bidirectional:
            other_cell.neighbors[direction.opposite()] = self

    def unlink_from(
        self, other_cell: "Cell", direction: Direction, bidirectional: bool = True
    ) -> None:
        if self.neighbors[direction] == other_cell:
            del self.neighbors[direction]

        if bidirectional and other_cell.neighbors[direction.opposite()] == self:
            del other_cell.neighbors[direction.opposite()]
