"""Puertos (interfaces) de la aplicación."""

from .capture_repository import CaptureRepository
from .spare_part_repository import SparePartRepository
from .species_repository import SpeciesRepository
from .user_repository import UserRepository

__all__ = [
    "UserRepository",
    "SpeciesRepository",
    "CaptureRepository",
    "SparePartRepository",
]
