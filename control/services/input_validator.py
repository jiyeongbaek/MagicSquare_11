"""Input validation service."""

from __future__ import annotations

from control.constants.error_codes import E_MATRIX_SIZE
from control.constants.matrix import MATRIX_SIZE


def validate_input(matrix: list[list[int]]) -> None:
    """Validate incoming matrix."""
    if len(matrix) != MATRIX_SIZE or any(len(row) != MATRIX_SIZE for row in matrix):
        raise ValueError(E_MATRIX_SIZE)

