"""Entidades del dominio."""

from .capture import Capture
from .spare_part import SparePart
from .species import Species
from .user import User

__all__ = ["User", "Species", "Capture", "SparePart"]
