"""Missing number finder service."""

from __future__ import annotations

from control.constants.matrix import MATRIX_SIZE

BLANK_VALUE = 0
MIN_CELL_VALUE = 1
MAX_CELL_VALUE = MATRIX_SIZE * MATRIX_SIZE


def find_missing_numbers(matrix: list[list[int]]) -> list[int]:
    """Find missing numbers from 1..16."""
    used_numbers = {value for row in matrix for value in row if value != BLANK_VALUE}
    all_numbers = set(range(MIN_CELL_VALUE, MAX_CELL_VALUE + 1))
    return sorted(all_numbers - used_numbers)

