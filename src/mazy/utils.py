from typing import TypeVar, Generator

T = TypeVar("T")


def consume_generator(generator: Generator[T, None, None]) -> T:
    """Generic generator consumer."""
    item = next(generator)
    while sentinel := next(generator, None):
        item = sentinel

    return item
