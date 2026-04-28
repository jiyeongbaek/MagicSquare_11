"""RED phase failing tests derived from PRD and README tasks.

These tests intentionally describe expected behavior before implementation.
Current placeholder services should cause these tests to fail.
"""

from __future__ import annotations

import pytest

from boundary.api.error_mapper import map_error
from boundary.api.response_mapper import map_solution_to_int6
from control.constants.error_codes import (
    E_BLANK_COUNT,
    E_DUPLICATE_NONZERO,
    E_MATRIX_SIZE,
    E_NO_VALID_COMBINATION,
    E_OUTPUT_FORMAT,
    E_VALUE_RANGE,
)
from control.services.blank_cell_finder import find_blank_cells
from control.services.combination_resolver import resolve_combination
from control.services.input_validator import validate_input
from control.services.missing_number_finder import find_missing_numbers
from entity.models.board import Board
from entity.rules.magic_sum_rule import is_magic_square
from entity.rules.uniqueness_rule import validate_nonzero_uniqueness
from entity.rules.value_range_rule import validate_value_range


def _valid_magic_with_two_blanks() -> list[list[int]]:
    return [
        [16, 2, 0, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 15, 0],
    ]


def test_task_001_board_creation_rejects_non_4x4_matrix() -> None:
    matrix = [[1, 2], [3, 4]]
    with pytest.raises(ValueError, match=E_MATRIX_SIZE):
        Board.from_matrix(matrix)


def test_task_002_board_rejects_out_of_range_values() -> None:
    matrix = _valid_magic_with_two_blanks()
    matrix[3][2] = 17
    assert validate_value_range(matrix) is False


def test_task_003_board_rejects_duplicate_nonzero_values() -> None:
    matrix = _valid_magic_with_two_blanks()
    matrix[3][2] = 16
    assert validate_nonzero_uniqueness(matrix) is False


def test_task_004_validate_input_rejects_invalid_blank_count() -> None:
    matrix = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 15, 1],
    ]
    with pytest.raises(ValueError, match=E_BLANK_COUNT):
        validate_input(matrix)


def test_task_005_find_blank_cells_returns_row_major_positions() -> None:
    matrix = _valid_magic_with_two_blanks()
    assert find_blank_cells(matrix) == [(0, 2), (3, 3)]


def test_task_005a_validate_input_rejects_non_4x4_matrix() -> None:
    matrix = [[1, 2], [3, 0]]
    with pytest.raises(ValueError, match=E_MATRIX_SIZE):
        validate_input(matrix)


def test_task_006_find_missing_numbers_returns_sorted_pair() -> None:
    matrix = _valid_magic_with_two_blanks()
    assert find_missing_numbers(matrix) == [1, 3]


def test_task_007_resolver_prefers_forward_combination_when_valid() -> None:
    matrix = _valid_magic_with_two_blanks()
    assert resolve_combination(matrix) == [1, 3, 3, 4, 4, 1]


def test_task_008_resolver_falls_back_to_reverse_combination() -> None:
    matrix = [
        [16, 0, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 0, 1],
    ]
    assert resolve_combination(matrix) == [1, 2, 2, 4, 3, 15]


def test_task_009_resolver_raises_no_valid_combination() -> None:
    matrix = [
        [16, 2, 0, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 0, 15],
    ]
    with pytest.raises(ValueError, match=E_NO_VALID_COMBINATION):
        resolve_combination(matrix)


def test_task_010_boundary_returns_whitelisted_error_codes_only() -> None:
    response = map_error("E_NOT_ALLOWED")
    allowed = {
        E_MATRIX_SIZE,
        E_BLANK_COUNT,
        E_VALUE_RANGE,
        E_DUPLICATE_NONZERO,
        E_OUTPUT_FORMAT,
        E_NO_VALID_COMBINATION,
    }
    assert response["code"] in allowed


def test_task_011_solver_output_matches_int6_schema() -> None:
    raw = [0, 0, 0]
    mapped = map_solution_to_int6(raw)
    assert len(mapped) == 6
    assert all(isinstance(value, int) for value in mapped)
    assert all(1 <= value <= 4 for value in (mapped[0], mapped[1], mapped[3], mapped[4]))


def test_red_guard_magic_square_judge_for_reference_case() -> None:
    complete = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 6, 12],
        [4, 14, 15, 1],
    ]
    assert is_magic_square(complete) is True

