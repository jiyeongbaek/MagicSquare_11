"""Blank cell finder service."""

from __future__ import annotations

from control.constants.matrix import MATRIX_SIZE

def find_blank_cells(matrix: list[list[int]]) -> list[tuple[int, int]]:
    """Find blank cells in row-major order."""
    blanks: list[tuple[int, int]] = []
    for row_idx in range(MATRIX_SIZE):
        for col_idx in range(MATRIX_SIZE):
            if matrix[row_idx][col_idx] == 0:
                blanks.append((row_idx, col_idx))
    return blanks

