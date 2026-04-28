"""Input validation service."""

from __future__ import annotations

from control.constants.error_codes import E_BLANK_COUNT, E_MATRIX_SIZE
from control.constants.matrix import MATRIX_SIZE

BLANK_VALUE = 0
REQUIRED_BLANK_COUNT = 2


def validate_input(matrix: list[list[int]]) -> None:
    """Validate incoming matrix."""
    if len(matrix) != MATRIX_SIZE or any(len(row) != MATRIX_SIZE for row in matrix):
        raise ValueError(E_MATRIX_SIZE)

    blank_count = sum(1 for row in matrix for value in row if value == BLANK_VALUE)
    if blank_count != REQUIRED_BLANK_COUNT:
        raise ValueError(E_BLANK_COUNT)

