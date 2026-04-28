"""Executable test suite derived from TC specification document.

This file is intentionally self-contained so the team can run and
experience the test scenarios immediately, even before production
modules are implemented.
"""

from __future__ import annotations

from typing import Iterable

import pytest

MAGIC_SUM = 34
VALID_ERROR_CODES = {
    "E_MATRIX_SIZE",
    "E_BLANK_COUNT",
    "E_VALUE_RANGE",
    "E_DUPLICATE_NONZERO",
    "E_OUTPUT_FORMAT",
    "E_NO_VALID_COMBINATION",
}


def validate_matrix(matrix: list[list[int]]) -> None:
    """Validate matrix invariants from the PRD.

    Args:
        matrix: Candidate 4x4 board.

    Raises:
        ValueError: If any invariant is violated.
    """
    if len(matrix) != 4 or any(len(row) != 4 for row in matrix):
        raise ValueError("E_MATRIX_SIZE")

    flat = [value for row in matrix for value in row]
    blank_count = flat.count(0)
    if blank_count != 2:
        raise ValueError("E_BLANK_COUNT")

    if any(value < 0 or value > 16 for value in flat):
        raise ValueError("E_VALUE_RANGE")

    non_zero = [value for value in flat if value != 0]
    if len(non_zero) != len(set(non_zero)):
        raise ValueError("E_DUPLICATE_NONZERO")


def find_blank_coords(matrix: list[list[int]]) -> list[tuple[int, int]]:
    """Return zero-based blank coordinates in row-major order."""
    coords: list[tuple[int, int]] = []
    for row_idx, row in enumerate(matrix):
        for col_idx, value in enumerate(row):
            if value == 0:
                coords.append((row_idx, col_idx))
    return coords


def find_missing_numbers(matrix: list[list[int]]) -> list[int]:
    """Find missing numbers from 1..16 and return sorted pair."""
    used = {value for row in matrix for value in row if value != 0}
    missing = sorted(set(range(1, 17)) - used)
    return missing


def is_magic_square(matrix: list[list[int]]) -> bool:
    """Check all row/col/diagonal sums are 34."""
    rows_ok = all(sum(row) == MAGIC_SUM for row in matrix)
    cols_ok = all(sum(matrix[row][col] for row in range(4)) == MAGIC_SUM for col in range(4))
    diag_main_ok = sum(matrix[i][i] for i in range(4)) == MAGIC_SUM
    diag_anti_ok = sum(matrix[i][3 - i] for i in range(4)) == MAGIC_SUM
    return rows_ok and cols_ok and diag_main_ok and diag_anti_ok


def _filled_matrix(
    matrix: list[list[int]],
    coords: Iterable[tuple[int, int]],
    values: Iterable[int],
) -> list[list[int]]:
    copied = [row[:] for row in matrix]
    for (r, c), value in zip(coords, values):
        copied[r][c] = value
    return copied


def resolve_combination(matrix: list[list[int]]) -> list[int]:
    """Resolve blanks by forward-first, reverse-fallback policy."""
    validate_matrix(matrix)
    coords = find_blank_coords(matrix)
    missing = find_missing_numbers(matrix)

    forward = _filled_matrix(matrix, coords, missing)
    if is_magic_square(forward):
        (r1, c1), (r2, c2) = coords
        n1, n2 = missing
        return [r1 + 1, c1 + 1, n1, r2 + 1, c2 + 1, n2]

    reverse = _filled_matrix(matrix, coords, list(reversed(missing)))
    if is_magic_square(reverse):
        (r1, c1), (r2, c2) = coords
        n1, n2 = list(reversed(missing))
        return [r1 + 1, c1 + 1, n1, r2 + 1, c2 + 1, n2]

    raise ValueError("E_NO_VALID_COMBINATION")


def _base_magic_square_with_two_blanks() -> list[list[int]]:
    return [
        [16, 2, 0, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 15, 0],
    ]


def test_tc_ms_a_001_blank_detection_basic() -> None:
    matrix = _base_magic_square_with_two_blanks()
    coords = find_blank_coords(matrix)
    assert coords == [(0, 2), (3, 3)]


def test_tc_ms_a_004_blank_detection_order_is_stable() -> None:
    matrix = _base_magic_square_with_two_blanks()
    assert find_blank_coords(matrix) == find_blank_coords(matrix) == find_blank_coords(matrix)


def test_tc_ms_a_005_rejects_invalid_blank_count() -> None:
    matrix = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 15, 1],
    ]
    with pytest.raises(ValueError, match="E_BLANK_COUNT"):
        validate_matrix(matrix)


def test_tc_ms_b_001_magic_square_success() -> None:
    matrix = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 15, 1],
    ]
    assert is_magic_square(matrix) is True


def test_tc_ms_b_002_magic_square_fail_on_row() -> None:
    matrix = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 15, 2],
    ]
    assert is_magic_square(matrix) is False


def test_tc_ms_c_001_missing_numbers_are_sorted() -> None:
    matrix = _base_magic_square_with_two_blanks()
    assert find_missing_numbers(matrix) == [1, 3]


def test_tc_ms_c_002_rejects_duplicate_nonzero() -> None:
    matrix = [
        [16, 2, 0, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 16, 0],
    ]
    with pytest.raises(ValueError, match="E_DUPLICATE_NONZERO"):
        validate_matrix(matrix)


def test_tc_ms_c_003_rejects_out_of_range_values() -> None:
    matrix = [
        [16, 2, 0, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 17, 0],
    ]
    with pytest.raises(ValueError, match="E_VALUE_RANGE"):
        validate_matrix(matrix)


def test_tc_ms_d_001_prefers_forward_combination_when_valid() -> None:
    matrix = _base_magic_square_with_two_blanks()
    result = resolve_combination(matrix)
    assert result == [1, 3, 3, 4, 4, 1]


def test_tc_ms_d_003_raises_when_no_valid_combination() -> None:
    matrix = [
        [16, 2, 0, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 0, 15],
    ]
    with pytest.raises(ValueError, match="E_NO_VALID_COMBINATION"):
        resolve_combination(matrix)


def test_tc_ms_d_004_result_schema_is_int6() -> None:
    matrix = _base_magic_square_with_two_blanks()
    result = resolve_combination(matrix)
    assert len(result) == 6
    assert all(isinstance(value, int) for value in result)


def test_tc_ms_d_005_result_coordinates_are_one_indexed() -> None:
    matrix = _base_magic_square_with_two_blanks()
    r1, c1, _, r2, c2, _ = resolve_combination(matrix)
    assert 1 <= r1 <= 4
    assert 1 <= c1 <= 4
    assert 1 <= r2 <= 4
    assert 1 <= c2 <= 4


def test_tc_ms_e_001_rejects_non_4x4_matrix() -> None:
    matrix = [[1, 2], [3, 0]]
    with pytest.raises(ValueError, match="E_MATRIX_SIZE"):
        validate_matrix(matrix)


def test_tc_ms_e_005_error_codes_use_whitelist() -> None:
    for code in VALID_ERROR_CODES:
        assert code.startswith("E_")
