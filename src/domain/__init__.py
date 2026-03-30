"""Módulo de dominio."""

from .exceptions import (
    CaptureNotFoundError,
    DomainException,
    InsufficientQuantityError,
    InvalidCaptureDataError,
    InvalidPasswordError,
    InvalidTokenError,
    SpeciesAlreadyExistsError,
    SpeciesHasCapturesError,
    SpeciesNotFoundError,
    SparePartNotFoundError,
    UnauthorizedAccessError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

__all__ = [
    "DomainException",
    "UserNotFoundError",
    "UserAlreadyExistsError",
    "InvalidPasswordError",
    "SpeciesNotFoundError",
    "SpeciesAlreadyExistsError",
    "SpeciesHasCapturesError",
    "CaptureNotFoundError",
    "InvalidCaptureDataError",
    "SparePartNotFoundError",
    "InsufficientQuantityError",
    "UnauthorizedAccessError",
    "InvalidTokenError",
]
