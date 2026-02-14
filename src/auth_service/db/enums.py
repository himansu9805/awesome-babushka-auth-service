"""Enums for auth service."""

from enum import Enum


class TokenType(Enum):
    """Enumeration for token types."""

    BEARER = "bearer"
    REFRESH = "refresh"
