"""Value range rule."""

from __future__ import annotations

from control.constants.matrix import MATRIX_SIZE

BLANK_VALUE = 0
MIN_NON_BLANK_VALUE = 1
MAX_CELL_VALUE = MATRIX_SIZE * MATRIX_SIZE


def validate_value_range(matrix: list[list[int]]) -> bool:
    """Return whether values are in allowed range."""
    return all(
        value == BLANK_VALUE or MIN_NON_BLANK_VALUE <= value <= MAX_CELL_VALUE
        for row in matrix
        for value in row
    )

