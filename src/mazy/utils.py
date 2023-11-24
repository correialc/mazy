"""Utility functions for general use."""
from typing import Generator, TypeVar, Optional

T = TypeVar("T")


def consume_generator(generator: Generator[T, None, Optional[T]]) -> T:
    """Generic generator consumer."""
    item = next(generator)
    while sentinel := next(generator, None):
        item = sentinel

    return item
