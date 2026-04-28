"""Boundary functions used by external interfaces (GUI/API/CLI)."""

from __future__ import annotations

from control.services.combination_resolver import resolve_combination
from control.services.input_validator import validate_input


def validate(matrix: list[list[int]]) -> None:
    """Validate matrix input against control-level invariants."""
    validate_input(matrix)


def solve(matrix: list[list[int]]) -> list[int]:
    """Solve matrix and return int[6] result contract."""
    return resolve_combination(matrix)

