"""Boundary response mapper."""

from __future__ import annotations

from control.constants.matrix import MATRIX_SIZE

RESULT_LENGTH = 6
DEFAULT_VALUE = 0
MIN_COORDINATE = 1
COORDINATE_INDEXES = (0, 1, 3, 4)


def map_solution_to_int6(solution: list[int]) -> list[int]:
    """Map solution payload to int[6] contract."""
    normalized = (solution + [DEFAULT_VALUE] * RESULT_LENGTH)[:RESULT_LENGTH]
    for coord_idx in COORDINATE_INDEXES:
        normalized[coord_idx] = min(MATRIX_SIZE, max(MIN_COORDINATE, normalized[coord_idx]))
    return normalized

