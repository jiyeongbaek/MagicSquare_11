"""Board entity model."""

from __future__ import annotations

from control.constants.error_codes import E_MATRIX_SIZE
from control.constants.matrix import MATRIX_SIZE


class Board:
    """Represents a 4x4 board."""

    def __init__(self, matrix: list[list[int]]) -> None:
        """Initialize board with raw matrix."""
        self.matrix = matrix

    @classmethod
    def from_matrix(cls, matrix: list[list[int]]) -> "Board":
        """Create a board instance from matrix input."""
        if len(matrix) != MATRIX_SIZE or any(len(row) != MATRIX_SIZE for row in matrix):
            raise ValueError(E_MATRIX_SIZE)
        return cls(matrix)

