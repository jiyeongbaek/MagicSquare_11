"""Combination resolver service."""

from __future__ import annotations

from control.constants.error_codes import E_NO_VALID_COMBINATION
from control.services.blank_cell_finder import find_blank_cells
from control.services.missing_number_finder import find_missing_numbers
from entity.rules.magic_sum_rule import is_magic_square


def _fill_matrix(
    matrix: list[list[int]],
    blanks: list[tuple[int, int]],
    values: list[int],
) -> list[list[int]]:
    copied = [row[:] for row in matrix]
    for (row_idx, col_idx), value in zip(blanks, values):
        copied[row_idx][col_idx] = value
    return copied


def resolve_combination(matrix: list[list[int]]) -> list[int]:
    """Resolve and return int[6] output."""
    (r1, c1), (r2, c2) = blanks = find_blank_cells(matrix)
    n1, n2 = missing = find_missing_numbers(matrix)

    forward_filled = _fill_matrix(matrix, blanks, missing)
    if is_magic_square(forward_filled):
        return [r1 + 1, c1 + 1, n1, r2 + 1, c2 + 1, n2]

    reversed_missing = list(reversed(missing))
    reverse_filled = _fill_matrix(matrix, blanks, reversed_missing)
    if is_magic_square(reverse_filled):
        rn1, rn2 = reversed_missing
        return [r1 + 1, c1 + 1, rn1, r2 + 1, c2 + 1, rn2]

    raise ValueError(E_NO_VALID_COMBINATION)

