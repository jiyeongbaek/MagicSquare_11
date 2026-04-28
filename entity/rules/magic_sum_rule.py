"""Magic sum judge rule."""

from __future__ import annotations

from magicsquare.domain import MAGIC_SUM, MATRIX_SIZE


def is_magic_square(matrix: list[list[int]]) -> bool:
    """Return whether matrix is a valid 4x4 magic square."""
    rows_ok = all(sum(row) == MAGIC_SUM for row in matrix)
    cols_ok = all(
        sum(matrix[row_idx][col_idx] for row_idx in range(MATRIX_SIZE)) == MAGIC_SUM
        for col_idx in range(MATRIX_SIZE)
    )
    main_diag_ok = sum(matrix[idx][idx] for idx in range(MATRIX_SIZE)) == MAGIC_SUM
    anti_diag_ok = sum(matrix[idx][MATRIX_SIZE - 1 - idx] for idx in range(MATRIX_SIZE)) == MAGIC_SUM
    return rows_ok and cols_ok and main_diag_ok and anti_diag_ok

