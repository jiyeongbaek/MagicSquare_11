"""Uniqueness rule for non-zero values."""

from __future__ import annotations

BLANK_VALUE = 0


def validate_nonzero_uniqueness(matrix: list[list[int]]) -> bool:
    """Return whether non-zero values are unique."""
    nonzero_values = [value for row in matrix for value in row if value != BLANK_VALUE]
    return len(nonzero_values) == len(set(nonzero_values))

