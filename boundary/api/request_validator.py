"""Boundary request validator."""

from __future__ import annotations


def validate_request(payload: object) -> list[list[int]]:
    """Validate request payload shape."""
    if not isinstance(payload, list):
        raise TypeError("payload must be list")
    return payload

