"""Magic sum judge rule."""

from __future__ import annotations

from magicsquare.domain import MAGIC_SUM, MATRIX_SIZE


def _sum_row(matrix: list[list[int]], row_idx: int) -> int:
    return sum(matrix[row_idx])


def _sum_col(matrix: list[list[int]], col_idx: int) -> int:
    return sum(matrix[row_idx][col_idx] for row_idx in range(MATRIX_SIZE))


def _sum_diag(matrix: list[list[int]], anti: bool = False) -> int:
    if anti:
        return sum(matrix[idx][MATRIX_SIZE - 1 - idx] for idx in range(MATRIX_SIZE))
    return sum(matrix[idx][idx] for idx in range(MATRIX_SIZE))


def is_magic_square(matrix: list[list[int]]) -> bool:
    """Return whether matrix is a valid 4x4 magic square."""
    rows_ok = all(_sum_row(matrix, row_idx) == MAGIC_SUM for row_idx in range(MATRIX_SIZE))
    cols_ok = all(_sum_col(matrix, col_idx) == MAGIC_SUM for col_idx in range(MATRIX_SIZE))
    main_diag_ok = _sum_diag(matrix) == MAGIC_SUM
    anti_diag_ok = _sum_diag(matrix, anti=True) == MAGIC_SUM
    return rows_ok and cols_ok and main_diag_ok and anti_diag_ok

