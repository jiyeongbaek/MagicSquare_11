"""Boundary error mapper."""

from __future__ import annotations

from control.constants.error_codes import (
    E_BLANK_COUNT,
    E_DUPLICATE_NONZERO,
    E_MATRIX_SIZE,
    E_NO_VALID_COMBINATION,
    E_OUTPUT_FORMAT,
    E_VALUE_RANGE,
)

ALLOWED_ERROR_CODES = {
    E_MATRIX_SIZE,
    E_BLANK_COUNT,
    E_VALUE_RANGE,
    E_DUPLICATE_NONZERO,
    E_OUTPUT_FORMAT,
    E_NO_VALID_COMBINATION,
}


def map_error(code: str) -> dict[str, str]:
    """Map internal error code to boundary payload."""
    mapped_code = code if code in ALLOWED_ERROR_CODES else E_OUTPUT_FORMAT
    return {"code": mapped_code, "message": mapped_code}

