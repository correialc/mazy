"""Tests for the utility functions."""
from typing import Generator

from mazy.utils import consume_generator


def test_utils_consume_generator() -> None:
    """Should consume a generator and return the final result."""

    def numbers(limit: int) -> Generator[int, None, None]:
        for i in range(limit + 1):
            yield i

    max_number = 3
    assert consume_generator(numbers(max_number)) == max_number
