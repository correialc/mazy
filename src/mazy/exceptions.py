"""Exceptions."""


class NeighborhoodError(Exception):
    """Consistence error between cells and directions."""


class DuplicatedNeighbor(Exception):
    """Raised when trying to link a cell to a neighbor that already exists."""


class MissingLink(Exception):
    """Raised when trying to unlink a cell and the link doesn't exist."""


class InvalidBuilder(Exception):
    """Invalid builder name provided."""


class InvalidViewer(Exception):
    """Invalid viewer name provided."""
