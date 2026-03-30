"""Rutas de la presentación."""

from .auth_routes import create_auth_routes
from .capture_routes import create_capture_routes
from .species_routes import create_species_routes
from .spare_part_routes import create_spare_part_routes
from .user_routes import create_user_routes

__all__ = [
    "create_auth_routes",
    "create_user_routes",
    "create_species_routes",
    "create_capture_routes",
    "create_spare_part_routes",
]
