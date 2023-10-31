from dataclasses import dataclass
from enum import IntEnum, IntFlag, auto


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


@dataclass(frozen=True)
class Cell:
    index: int
    row: int
    col: int
    border: Border = Border.EMPTY
    role: Role = Role.NONE
