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


def _try_placement(
    matrix: list[list[int]],
    blanks: list[tuple[int, int]],
    values: list[int],
) -> list[int] | None:
    filled = _fill_matrix(matrix, blanks, values)
    if not is_magic_square(filled):
        return None

    (r1, c1), (r2, c2) = blanks
    n1, n2 = values
    return [r1 + 1, c1 + 1, n1, r2 + 1, c2 + 1, n2]


def resolve_combination(matrix: list[list[int]]) -> list[int]:
    """Resolve and return int[6] output."""
    blanks = find_blank_cells(matrix)
    missing = find_missing_numbers(matrix)

    forward_result = _try_placement(matrix, blanks, missing)
    if forward_result is not None:
        return forward_result

    reversed_missing = list(reversed(missing))
    reverse_result = _try_placement(matrix, blanks, reversed_missing)
    if reverse_result is not None:
        return reverse_result

    raise ValueError(E_NO_VALID_COMBINATION)

