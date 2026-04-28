"""Board entity model."""

from __future__ import annotations


class Board:
    """Represents a 4x4 board."""

    def __init__(self, matrix: list[list[int]]) -> None:
        """Initialize board with raw matrix."""
        self.matrix = matrix

    @classmethod
    def from_matrix(cls, matrix: list[list[int]]) -> "Board":
        """Create a board instance from matrix input."""
        return cls(matrix)

