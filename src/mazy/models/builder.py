"""Models related to maze builders."""
from enum import Enum


class BuilderAlgorithm(Enum):
    """Maze builder algorithms domain."""

    DUMMY = "dummy"
    BINARY_TREE = "binary-tree"
    SIDEWINDER = "sidewinder"
