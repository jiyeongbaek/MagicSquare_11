"""Boundary error mapper."""

from __future__ import annotations


def map_error(code: str) -> dict[str, str]:
    """Map internal error code to boundary payload."""
    return {"code": code, "message": code}

